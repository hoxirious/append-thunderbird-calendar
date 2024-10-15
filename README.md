# append-thunderbird-calendar
Extract time schedule information from email and create events on Thunderbird Calendar

# Inspiration
I came across this series [PDF Parser in C](https://www.youtube.com/watch?v=ZYBRiEpdpCY&list=PLwHDUsnIdlMxLFqB0YtFWzwl1VogDCrDY) on youtube. It really inspired me on getting better as a Software Engineer. The way he approaches the problems, and resolves them without the help of LLM or Google is exactly how an engineer should strive for. The only resource that he needs was the documentation on Wikipedia and no library. Watching him coding, I asked myself if I am able to do something like that. That is the main reason why this tool is developed. 

# Features
This script covers:
- Date formats: ddmmyyyy, yyyymmdd, Day Month Year.
- Simple language: "This/Next" + Day. E.g. Next Friday.
- Timezone conversion.
- Multiple events creation.
