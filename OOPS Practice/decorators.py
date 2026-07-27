from functools import wraps

def my_logger(original_function):
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__),level = logging.INFO)
    
    @wraps(original_function)
    def wrapper(*args,**kwargs):
        logging.info(
            "Ran with args: {} and kwargs: {}".format(args,kwargs))
        return original_function(*args,**kwargs)
    
    return wrapper


def my_timer(original_function):
    import time
    
    @wraps(original_function)
    def wrapper(*args,**kwargs):
        t1 = time.time()
        result = original_function(*args,**kwargs)
        t2 = time.time() - t1
        
        print("{} ran for {} secs".format(original_function.__name__,t2))
        return result
    
    return wrapper

def retry(n):
    def decorator_function(original_function):
        @wraps(original_function)
        def wrapper(*args,**kwargs):
            attempt = 1
            while attempt <= n:
                try:
                    result = original_function(*args,**kwargs)
                    return result        #Success
                except Exception as e:
                    print("Retrying: Attempt ",attempt,"/",n)
                    attempt += 1
                    
                    if attempt > n:
                        raise e
                
        return wrapper
    return decorator_function
                

@retry(3)
def test():
    raise ValueError("Something went wrong")

test()
    
        
# import time

# @my_timer
# def display_info(name, age):
#     time.sleep(1)
#     print('display_info ran with arguments ({}, {})'.format(name, age))

# display_info('Dhoni', 37)