# Hello-world

Simple initial challenge to verify that the environment is working correctly.

### Tasks

1. **Submission test**
   - Just submit a "BSY{hello-world}" as a flag to test the dashboard.

2. **Hackerlab test**
   - Find a flag in your hackerlab home directory
   - Use commands like `ls -la`, `find`, or `grep` to locate it
   - The flag is hidden in a file in your home directory

3. **Network test**
   - Find an HTTP server running at IP address `172.30.0.5`
   - Use `nmap` to scan for open ports
   - Use `curl` to retrieve the flag

## How to solve
<details>
  <summary>Click to reveal how to solve steps</summary>

1. For the Network test, use `nmap` to find opened ports:
```bash
root@hackerlab:~# nmap -sS -n -v 172.30.0.5   
...
PORT     STATE SERVICE
8000/tcp open  http-alt
MAC Address: 36:A1:91:58:A6:BF (Unknown)
...
```

2. Discover opened port 8000 and try to send an HTTP request
```bash
root@hackerlab:~# curl 172.30.0.5:8000 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello world</title>
</head>
<body>
    Congratulations, you found a flag for the hello-world challenge. 
    Your setup seems to be working, happy hacking!
    
    BSY{simple-hello-world-flag}
</body>
</html>
```

3. For the Hackerlab test, try these commands:
```bash
# List all files including hidden ones
ls -la

# Search for files containing "BSY"
find /root -type f -exec grep -l "BSY" {} \;

# Or directly look for the flag file
find /root -name ".flag.txt"
```

</details>

## Testing

The script [auto-solve.sh](./auto-solve.sh) automatically verifies that the challenge can be solved.
