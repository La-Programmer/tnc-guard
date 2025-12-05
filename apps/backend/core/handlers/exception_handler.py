from fastapi import Request


async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global exception handler triggered.....")
    print("\n\n---------------------------------------------")
    print(f"\nRequest: {request}")
    print(f"\nException: {exc}")
