#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 16:27
# @Author  : SayHeya
# @File    : status.py
# @Contact : sayheya@qq.com
# @Desc    : All variable's status should be defined here!!!!


class StatusType(type):
    def __contains__(cls, item):
        return item in cls.keys or item in cls.values

    @property
    def keys(cls):
        return [k for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def values(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def items(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('__')}


class TaskStatus(metaclass=StatusType):
    ok = 0
    failed = 1
    unknown = -1


if __name__ == '__main__':
    print(TaskStatus.keys)
    print(TaskStatus.values)
    print(TaskStatus.items)
