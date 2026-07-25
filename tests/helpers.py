# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT


def nop(*_, **__):
    pass


class CloseMe:
    is_closed = False

    def close(self):
        self.is_closed = True
