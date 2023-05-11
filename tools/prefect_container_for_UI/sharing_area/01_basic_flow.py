from prefect import flow
import time

@flow
def my_favorite_function():
    print("What is your favorite number?")    
    time.sleep(10)
    print("waited 10")
 
    return 42

print(my_favorite_function())
