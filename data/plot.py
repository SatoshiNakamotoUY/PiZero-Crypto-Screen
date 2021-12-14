import math
from datetime import datetime
from config.config import config

class Plot:
    @staticmethod
    def line(prices, size=(100, 100), position=(0, 0), draw=None, fill=None):
        assert draw
        max_price = max(prices)
        min_price = min(prices)
        normalised_prices = [(price - min_price) / (max_price - min_price) for price in prices]
        plot_data = []
        plot_data.append((position[0],size[1]))
        for i, element in enumerate(normalised_prices):
            x = i * (size[0] / len(normalised_prices)) + position[0]
            y = size[1] - (element * size[1]) + position[1]
            plot_data.append((x, y))
        plot_data.append(((size[0] / len(normalised_prices))*(len(normalised_prices)-1)+position[0],size[1]))
        #draw.line(plot_data, fill=fill)
        draw.polygon(plot_data, fill=fill)
        try:
            plot_data.pop(0)
            plot_data.pop()
        except IndexError as e:
            logger.error(str(e))
        draw.line(plot_data, fill="#000000")

    @staticmethod
    def date_labels(prices, font, position_first=(0, 0), position_last=(0, 0), draw=None, fill=None):
        def human_date(timestamp):
            #return datetime.fromtimestamp(timestamp/1000).strftime('%d %b')
            return datetime.fromtimestamp(timestamp/1000).strftime('%d %b %H:%M')

        text_width, _ = draw.textsize(human_date(prices[1]), font)
        price_position = ((position_last[0] - text_width), position_last[1])

        draw.text(position_first, human_date(prices[0]), font=font, fill=fill)
        draw.text(price_position, human_date(prices[1]), font=font, fill=fill)


    # TODO: Implement variable number of elements to generate
    @staticmethod
    def y_axis_labels(prices, font, position_first=(0, 0), position_last=(0, 0), draw=None, fill=None):
        def center_x(price):
            area_width = position_last[0] - position_first[0]
            text_width, _ = draw.textsize(price, font)
            if area_width >= text_width:
                return position_first[0] + (area_width - text_width) / 2
            else:
                return position_first[0]

        max_price = max(prices)
        min_price = min(prices)
        middle_price = (max_price - min_price) / 2 + min_price

        price = Plot.human_format(max_price, 5)
        draw.text((center_x(price), position_first[1]), price, font=font, fill=fill)
        price = Plot.human_format(middle_price, 5)
        draw.text((center_x(price), (position_last[1] - position_first[1]) / 2 + position_first[1]), price, font=font, fill=fill)
        price = Plot.human_format(min_price, 5)
        draw.text((center_x(price), position_last[1]), price, font=font, fill=fill)

    @staticmethod
    def caption(coin, price, y, screen_width, font, draw, fill=None, currency_offset=-1, price_offset=80):
        draw.text((currency_offset, y), coin[:4], font=font, fill=fill)
        price_text = Plot.human_format(price, 8, 2)
        text_width, _ = draw.textsize(price_text, font)
        # price_position = (((screen_width - text_width - price_offset) / 2) + price_offset, y)
        price_position = ((screen_width - text_width), y)
        draw.text(price_position, price_text, font=font, fill=fill)

    @staticmethod
    def candle(data, size=(100, 100), position=(0, 0), draw=None, fill_neg="#000000", fill_pos=None):
        width = size[0]
        height = size[1]
        candle_width = 5
        space = 1
        windows_per_candle = 1
        data_offset = 0
        candle_data = []

        num_of_candles = width // (candle_width + space)
        leftover_space = width % (candle_width + space)

        if num_of_candles < len(data):
            windows_per_candle = len(data) // num_of_candles
            data_offset = len(data) % num_of_candles

        #date_data.append(datetime.fromtimestamp(data[data_offset][0]/1000).strftime('%d %b %H:%M'))
        #date_data.append(datetime.fromtimestamp(data[len(data)-1][0]/1000).strftime('%d %b %H:%M'))

        for i in range(data_offset, len(data), windows_per_candle):
            if windows_per_candle > 1:
                window = data[i:i + windows_per_candle - 1]
                open = window[0][0]
                close = window[len(window) - 1][3]
                high = max([i[1] for i in window])
                low = min([i[2] for i in window])
            else:
                open = data[i][0]
                close = data[i][3]
                high = data[i][1]
                low = data[i][2]
            candle_data.append((open, high, low, close))

        all_values = [item for sublist in candle_data for item in sublist]
        max_price = max(all_values)
        min_price = min(all_values)

        normalised_data = []
        for line in candle_data:
            normalised_line = []
            normalised_data.append(normalised_line)
            for i in range(len(line)):
                price = line[i]
                normalised_line.append((price - min_price) / (max_price - min_price))

        def y_flip(y):
            return height - (y * height) + position[1]

        for i, element in enumerate(normalised_data):
            open = element[0]
            close = element[3]
            high = element[1]
            low = element[2]
            x = candle_width * i + space * i + leftover_space / 2 + position[0]
            # high price
            wick_x = x + (candle_width // 2)
            draw.line([wick_x, y_flip(high), wick_x, y_flip(max(open, close))], fill=fill_pos)
            # low price
            draw.line([wick_x, y_flip(low), wick_x, y_flip(min(open, close))], fill=fill_pos)

            open_y = math.floor(y_flip(open))
            close_y = math.floor(y_flip(close))
            if open_y == close_y:
                draw.line([x, open_y, x + candle_width - 1, close_y], fill=fill_pos)
            else:
                if open < close:
                    draw.rectangle([x, open_y, x + candle_width - 1, close_y], fill=fill_pos)
                else:
                    draw.rectangle([x, open_y, x + candle_width - 1, close_y], fill=fill_neg)

    # TODO: Adapt for big numbers 1k, 1m, etc
    @staticmethod
    def human_format(number, length, fractional_minimal=0):
        magnitude = 0
        num = number
        while abs(num) >= 10:
            magnitude += 1
            num /= 10.0
        format_string = f'%.{fractional_minimal}f'
        if length >= magnitude + fractional_minimal + 2:
            fractional_length = length - magnitude - 2
            format_string = f'%.{fractional_length}f'
        return format_string % number
