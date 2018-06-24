# https://www.youtube.com/watch?v=8FdeJ2_LDuQ


import asyncio

loop = asyncio.get_event_loop()


# Option 1
async def hello():
    print('Hello')
    await asyncio.sleep(3)
    print('World!')


# Option 2
# @asyncio.coroutine
# def hello():
#     print('Hello')
#     yield from asyncio.sleep(3)
#     print('World!')

if __name__ == '__main__':
    loop.run_until_complete(hello())
