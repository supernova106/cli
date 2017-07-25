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

- packages

```
yum list installed
yum list packageName
yum remove packageName
# OR
dpkg -l
dpkg -i packageName
apt-get remove packageName
apt-cache policy packageName
```

-

```
# Scanning for a single port
nmap -p portnumber hostname
# Scan entire machine for checking open ports.
nmap hostname
# Scan entire network for open ports
nmap network ID/subnet-mask
# Scan the machine and give as much details as possible
nmap -v hostname
# Scan a machine for TCP/UDP open ports
nmap -sT hostname
nmap -sU hostname
# To check which protocol(not port) such as TCP, UDP, ICMP ...
nmap -sO hostname
```

- Check disk usage based on folder with depth (d), human readable(h)

```
du -h -d 1
sudo du -hs * | sort -rh | head -5
sudo find . -mtime +14 -exec rm -ir {} \;
# Get all files older than X days. Add -delete at the end to remove the result.
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
# find php.ini
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
w
uptime
```

- troubleshoot

```
netstat -lntpu
ps aux
ps -ef
lsof -p
lsof -u
# List currently established, closed, orphaned and waiting TCP sockets, enter:
ss -s
# Display All Open Network Ports
ss -l
# see process named using open socket:
ss -pl
# Display All TCP Sockets
ss -t -a
# Display All UDP Sockets
ss -u -a
# Display All UNIX Sockets
ss -x -a
# Display All Established HTTP Connections
ss -o state established '( dport = :http or sport = :http )'
# Find All Local Processes Connected To X Server
ss -x src /tmp/.X11-unix/*
# List all the TCP sockets in state -FIN-WAIT-1 for our httpd to network 202.54.1/24 and look at their timers:
ss -o state fin-wait-1 '( sport = :http or sport = :https )' dst 202.54.1/24
## tcp ipv4 ##
ss -4 state FILTER-NAME-HERE
## tcp ipv6 ##
ss -6 state FILTER-NAME-HERE
## Show all ports connected from remote 192.168.1.5##
ss dst 192.168.1.5
## show all ports connected from remote 192.168.1.5:http port##
ss dst 192.168.1.5:http
ss dst 192.168.1.5:smtp
ss dst 192.168.1.5:443
pidstat 1
iostat -zx 1
```

- FILTER-NAME-HERE

```
established
syn-sent
syn-recv
fin-wait-1
fin-wait-2
time-wait
closed
close-wait
last-ack
listen
closing
all : All of the above states
connected : All the states except for listen and closed
synchronized : All the connected states except for syn-sent
bucket : Show states, which are maintained as minisockets, i.e. time-wait and syn-recv.
big : Opposite to bucket state.

```

- top

```
Key Switches For The Top Command:
-h - Show the current version
-c - This toggles the command column between showing command and program name
-d - Specify the delay time between refreshing the screen
-o - Sorts by the named field
-p - Only show processes with specified process IDs
-u - Show only processes by the specified user
-i - Do not show idle tasks
```

```
A	Alternative display (default off)
d	Refresh screen after specified delay in seconds (default 1.5 seconds)
H	Threads mode (default off), summarises tasks
p	PID Monitoring (default off), show all processes
B	Bold enable (default on), values are shown in bold text
l	Display load average (default on)
t	Determines how tasks are displayed (default 1+1)
m	Determines how memory usage is displayed (default 2 lines)
1	Single cpu (default off) - i.e. shows for multiple CPUs
J	Align numbers to the right (default on)
j	Align text to the right (default off)
R	Reverse sort (default on) - Highest processes to lowest processes
S	Cumulative time (default off)
u	User filter (default off) show euid only
U	User filter (default off) show any uid
V	Forest view (default on) show as branches
x	Column highlight (default off)
z	Color or mono (default on) show colors
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

## LDAP/SSSD

- Kerberos

```
# krb5
klist
klist -t -k /etc/krb5.keytab
kinit -p [user]@[domain]
```

- LDAP

```
ldapsearch -x -LLL -h [host] -D [user] -w [password] -b cn=Users,dc=corp,dc=ebates,dc=com -s sub "(objectClass=user)" givenName
```

- join AD

```
domainjoin-cli join secure.local domain-bind
```

## Nagios

- plugins: `/usr/local/nagios/plugins/`
- check syntax `/usr/local/nagios/bin/nagios -v /etc/nagios.cfg`

## Security

- NTP

```
# Solution
restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
# Test mode 6 query:
ntpq -c rv <IP>
# Check NTP status:
ntpd --version
timedatectl status
# monlist attack
ntpdc -n -c monlist localhost
ntpdc -c sysinfo
```
- SSH

```
sudo sshd -T |grep ciphers => ciphers aes256-ctr
add "ciphers aes256-ctr" to "/etc/ssh/sshd_config", restart sshd service
```
## Contact

Binh Nguyen
