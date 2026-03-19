import subprocess
import time
import os

# The list of URLs you want to process
urls = [
    "https://el.wikipedia.org/wiki/Θεσσαλονίκη",
    "https://el.wikipedia.org/wiki/Ρώμη",
    "https://el.wikipedia.org/wiki/Παρίσι",
    "https://el.wikipedia.org/wiki/Νέα_Υόρκη",
    "https://el.wikipedia.org/wiki/Τόκιο",
    "https://el.wikipedia.org/wiki/Βαρκελώνη",
    "https://el.wikipedia.org/wiki/Σικάγο",
    "https://el.wikipedia.org/wiki/Λονδίνο",
    "https://el.wikipedia.org/wiki/Σιγκαπούρη",

]

def run_tests():

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for url in urls:
        print(f"Launching app.py for: {url}")
        
        process = subprocess.run(
            ['python', 'app.py'],
            input=url,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env
        )

        if process.stdout:
            print(process.stdout)
        
        if process.stderr:
            print(f"Error in this run: {process.stderr}")
            
        print("-" * 40)
        
        time.sleep(10)

if __name__ == "__main__":
    run_tests()