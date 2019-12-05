from .. import unicode


class State:
    def __init__(self, bar_width, cursor_width=3, fill=unicode.FULL_BLOCK, empty=' ', prefix='[', postfix=']'):

        if type(bar_width) != int:
            raise TypeError('bar width must be of type int')

        if bar_width <= 0:
            raise ValueError('bar width must be greater that 1')

        if type(cursor_width) != int:
            raise TypeError('cursor width must be of type int')

        if cursor_width <= 0:
            raise ValueError('cursor width must be greater that 0')

        if bar_width < cursor_width:
            raise ValueError('cursor width must be greater than bar width')

        self.width = bar_width
        self.cursor_width = cursor_width
        self.fill = fill
        self.empty = empty

        self.prefix = prefix
        self.postfix = postfix

        # generate states
        self.states = []

        # all the generation math
        snake = list((self.fill * cursor_width) + (self.empty * (bar_width * 2)))
        fallout_start = self.cursor_width - 1
        fallout_end = self.width + self.cursor_width - 1

        i = 0
        while True:
            segment = snake[fallout_start:fallout_end]
            self.states.append(f"{prefix}{''.join(segment)}{postfix}")

            if all(bit == self.empty for bit in segment):
                break

            # crawl forward
            bit = snake.pop(-1)
            snake.insert(0, bit)

            i += 1

        # debugging
        # for state in self.states:
        #     print(f'{state}')
        #
        # print('[', end='')
        # for i in range(self.width):
        #     print(i % 10, end='')
        # print(']')
        #
        # print({'start': fallout_start, 'end': fallout_end, 'width': fallout_end - fallout_start})
