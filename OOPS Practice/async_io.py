import asyncio
import time

async def say_after(delay,what):
    await asyncio.sleep(delay)
    print(what)
    
#Running both the tasks one after another - Non Concurrent
# async def main1():
#     print(f"started at {time.strftime('%X')}")

#     await say_after(1, 'hello')
#     await say_after(2, 'world')

#     print(f"finished at {time.strftime('%X')}")

# asyncio.run(main1())
    
    
#Running processes concurrently using create_task()
# async def main2():
    
#     task1 = asyncio.create_task(say_after(1,"Hello"))
#     task2 = asyncio.create_task(say_after(2,"World"))
    
#     print(f"Started at {time.strftime('%X')}")
    
#     await task1
#     await task2
    
#     print(f"Finished at {time.strftime('%X')}")
    
# asyncio.run(main2())


async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")
    
asyncio.run(main())