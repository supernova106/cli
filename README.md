## AWS
- get AMI ID based on name `aws ec2 describe-images --region=us-east-1 --filters "Name=name,Values=AMI_NAME" | grep ImageId | awk  '{print $2}' | cut -d\" -f2`

## Linux CLI

- Monitoring user

```
finger username
id username
chage -l username
groups username
```

- Scanning for a single port 

```
nmap -p portnumber hostname
```

- Scan entire machine for checking open ports.

```
nmap hostname
```

- Scan entire network for open ports

```
nmap network ID/subnet-mask
```

- Scan the machine and give as much details as possible

```
nmap -v hostname
```

- Scan a machine for TCP/UDP open ports

```
nmap -sT hostname
nmap -sU hostname
```

-  To check which protocol(not port) such as TCP, UDP, ICMP ...

```
nmap -sO hostname
```

- Check disk usage based on folder with depth (d), human readable(h)

```
du -h -d 1
```

- Get all files older than X days. Add -delete at the end to remove the result.

```
find * -type f -mtime +X -delete
```

- get PHP modules extension

```
grep -Hrv ";" /etc | grep -i "extension="
-r or -R is recursive,
-n is line number, and
-w stands match the whole word.
-l (lower-case L) can be added to just give the file name of matching files.
Along with these, --exclude or --include parameter could be used for efficient searching. Something like below:
grep --include=\*.{c,h} -rnw '/path/to/somewhere/' -e "pattern"
```

- find php.ini

```
php -i | grep "Loaded Configuration File"
```

- check OS type

```
uname -a
```

- check filesystem

```
file -s /dev/<device>
```

- check all crontabs

```
crontab -l
crontab -u username -l
```

- stress CPU

```
stress --cpu 2 --timeout 60
```

- view load average

```
uptime
```

- troubleshoot

```
pidstat 1
iostat -zx 1
```

- network interface throughput: rzkb/s and txkb/s

```
sar -n DEV 1
```

## MySQL

- Duplicate schema based on other schema

```
mysqldump -h [server] -u [user] -p[password] db1 | mysql -h [server] -u [user] -p[password] db2
```

- Create User

```
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
```

- See full query

```
mysql>SHOW FULL PROCESSLIST;
```

- Output SQL query to CSV

```
mysql -h <host> -u <user_name> -p <pass_word> DB -e "QUERY" >> result.csv;
sed -i 's/\t/,/g' result.csv
```

## Git

```
# add new origin
git remote add origin <origin>
# modify origin
git remote set-url origin
# reset
git reset HEAD --hard
# switch branch
git checkout <branch>
```

## Docker

```
# interactive docker container
docker exec -it <docker_id> bash
docker exec -it --user root <docker_id> bash
# Remove all untagged images
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
# Remove stopped containers
docker rm $(docker ps -a | grep Exited | awk '{print $1}')
# Run multiple bash commands in one docker command
docker run (image) sh -c "cmd1 && cmd2 && cmd3"
# entrypoint
ENTRYPOINT ["executable", "param1", "param2"]
```

## Ansible

```
# common
ansible all -m shell -a "ls -la"
# Ensure a service is started on all webservers
ansible webservers -m service -a "name=httpd state=started"
```

## OpenVPN

```
# login with openvpn client
openvpn --config xxx.ovpn
```

## Contact

Binh Nguyen
