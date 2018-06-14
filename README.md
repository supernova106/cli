## AWS
- get AMI ID based on name `aws ec2 describe-images --region=us-east-1 --filters "Name=name,Values=AMI_NAME" | grep ImageId | awk  '{print $2}' | cut -d\" -f2`
- export list ec2 instances to excel sheet

```
ec2 describe-instances --output text --query 'Reservations[*].Instances[*].[InstanceId, InstanceType, ImageId, State.Name, LaunchTime, Placement.AvailabilityZone, Placement.Tenancy, PrivateIpAddress, PrivateDnsName, PublicDnsName, [Tags[?Key==`Name`].Value] [0][0], [Tags[?Key==`purpose`].Value] [0][0], [Tags[?Key==`environment`].Value] [0][0], [Tags[?Key==`team`].Value] [0][0] ]' > instances.tsv
# open instances.tsv with Excel
# enjoy
```

- user-data

```
curl http://169.254.169.254/latest/user-data
```

- iam 

```
curl http://169.254.169.254/latest/meta-data/iam/info
```

## Docker

Containers

- Containers should be ephemeral.
- Use a .dockerignore file.
- Use multi-stage builds.
- Avoid installing unnecessary packages.
- Each container should have only one concern.
- Minimize the number of layers.
- Sort multi-line arguments.
- Build cache.
- Don’t trust arbitrary base images.
- Use small base image.
- Use the builder pattern.

Inside Container

- Use non-root user inside container.
- Make the file system read only.
- One process per container.
- Don’t restart on failure, crash cleanly instead.
- Log to stdout & stdderr
- Add dumb-init to prevent zombie processes.

Deployment

- Use the “record” option for easier rollbacks.
- Use plenty of descriptive labels.
- Use sidecar containers for proxies , watchers etc.
- Don’t use sidecar for bootstrapping.
- Use init container instead.
- Don’t Use latest or no tag.
- Readness & liveness probes are your friends.

Security Best Practices

- Ensure That Images Are Free of Vulnerabilities.
- Ensure That Only Authorized Images are Used in Your Environment.
- Limit Direct Access to Kubernetes Nodes.
- Create Administrative Boundaries between Resources.
- Define Resource Quota.
- Implement Network Segmentation.
- Apply Security Context to Your Pods and Containers.
- Log Everything.
- Integrate Security into your CI/CD pipeline
- Implement Continuous Security Vulnerability Scanning
- Regularly Apply Security Updates to Your Environment.
- Use private registries to store your approved images.
- Make sure you only push approved images to these registries

Services:-

- Don’t always use type: LoadBalancer
- Ingress is great
- Type: NodePort is good enough.
- Use static IP, they are free.
- Map external service to internal ones.

Application architecture

- Use helmchart
- ALL downstream dependencies are unreliable.
- Make sure you micro-service aren’t too micro.
- Use service mesh.

Cluster Management

- Use Google container engine
- Resources, anti-afinity & scheduling.
- Use Namespace to split up your cluster.
- Role base access control.
- Unleash the chaos monkey.
- Limit SSH access to Kubernetes nodes, Ask users to use “kubectl exec”
- Create administrative boundaries between resources.
- Implement Network segmentation.

Monitoring and visibility:-

- Cluster-based logging
- Log container activity into a central log hub.
- Use Fluentd agent on each node
- Ingested logs using Google Stackdriver Logging
- Elasticsearch Viewed with Kibana.

## Chef

- create org

```
chef-server-ctl org-create name "NICE NAME"
```

- create new user

```
chef-server-ctl  user-create lolha Lol Ha lolha@example.com password -f /root/pem/lolha.pem
```

- grant admin access to an organization

```
chef-server-ctl org-user-add techops lolha --admin
```

## Linux CLI

- Insert on ignore to a text file

```
grep -q -F 'BLAH BLHA "BLOH"' /etc/hosts || echo 'BLAH BLHA "BLOH"' >> /etc/hosts
```

- Find Outbound Public IP address

```
curl -s http://ipchicken.com | egrep -o '([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}'
```

- run command line with argument from line of a text file `<file.txt xargs -I % <commmand> %`
- key pem to JSON `sed ':a;N;$!ba;s/\n/\\n/g' my_key.pem`
- get the error log within an amount of time

```
awk -v d1="$(date --date="-2 min" "+%b %_d %H:%M")" -v d2="$(date "+%b %_d %H:%M")" '$0 > d1 && $0 < d2 || $0 ~ d2' /var/log/usc/uscapp.log | egrep -i '(false|ERROR)'
```

- total memory

```
free -mh | egrep -o '^Mem:\s*([0-9].[0-9]G)' | cut -d':' -f2 | tr -d ' '
```

- Monitoring user

```
finger username
id username
chage -l username
groups username
```

- file transfer

```
/usr/bin/rsync -Pau -e "ssh -i $HOME/.ssh/[private_key]"  [username]@[host]:/path/*.war $HOME/dest/
```

- sendmail

```
# cd /var/spool/mqueue
# grep -l "No acceptable" * | xargs -I {} rm {}
# grep -l "admin1" * | xargs -I {} rm {}
# grep -l "admin2" * | xargs -I {} rm {}
# grep -l "amandabackup" * | xargs -I {} rm {}
# no. of mails in the queue
sendmail -bp
# cleanup
/var/spool/mqueu*
find . -type f | xargs rm -rf
# user mailbox
/var/mail/
```

- PBIS Open

```
/opt/pbis/bin/get-status
/opt/pbis/bin/find-objects --user <user_name>
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

- Ubuntu 16.04 use systemd, (runlevel only exists in init system)
```
   Mapping between runlevels and systemd targets
   ┌─────────┬───────────────────┐
   │Runlevel │ Target            │
   ├─────────┼───────────────────┤
   │0        │ poweroff.target   │
   ├─────────┼───────────────────┤
   │1        │ rescue.target     │
   ├─────────┼───────────────────┤
   │2, 3, 4  │ multi-user.target │
   ├─────────┼───────────────────┤
   │5        │ graphical.target  │
   ├─────────┼───────────────────┤
   │6        │ reboot.target     │
   └─────────┴───────────────────┘
```

- top

```
top -o %MEM # Sort by memory usage
top -o %CPU # Sort by cpu usage

# Shift + F to display help

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

```shell
sar -n DEV 1
```

## Locale

Fix locale issue

```shell
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
```

## Screen

```shell
screen
Ctrl + A and ?
# detach
d
# restore
screen -r
screen -ls
screen -r [id]
# view screen from other user
script /dev/null
screen -r
```

## SSL

- generate SSL self-signed cert

```shell
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt
```

- copy self-signed CA cert to `/usr/local/share/ca-certificates/`
- run `sudo update-ca-certificates`
- verify that you can find the new certificate in `/etc/ssl/certs/ca-certificates.crt`
- retrieve public cert via openssl

```shell
ex +'/BEGIN CERTIFICATE/,/END CERTIFICATE/p' <(echo | openssl s_client -showcerts -connect www.example.com:443) -scq > file.crt
```

```
openssl s_client -connect <host>:<port>
# Check a certificate and return information about it (signing authority, expiration date, etc.):
openssl x509 -in server.crt -text -noout
# Check the SSL key and verify the consistency:
openssl rsa -in server.key -check
# Verify the CSR and print CSR data filled in when generating the CSR:
openssl req -text -noout -verify -in server.csr
# These two commands print out md5 checksums of the certificate and key; the checksums can be compared to verify that the certificate and key match.
openssl x509 -noout -modulus -in server.crt| openssl md5
openssl rsa -noout -modulus -in server.key| openssl md5
```

## MySQL

- Duplicate schema based on other schema

```
mysqldump -h [server] -u [user] -p[password] db1 | mysql -h [server] -u [user] -p[password] db2
```

- Create User

```
CREATE USER 'grafana'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON grafana . * TO 'grafana'@'%';
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
# tracking git commits to a file
git log --follow filename
# compare the diff in a commit
git diff COMMIT^ COMMIT
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

## Consul

Check node status

```
curl http://127.0.0.1:8500/v1/health/node/<node_name>
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

- SSSD debugging `sudo sssd -d9 -i`
- LDAP

```
ldapsearch -x -LLL -h [host] -D [user] -w [password] -b cn=Users,dc=corp,dc=ebates,dc=com -s sub "(objectClass=user)" givenName
# with SSL/TLS
ldapsearch -x -ZZ -LLL -h [host] -D [user] -w [password] -b cn=Users,dc=corp,dc=ebates,dc=com -s sub "(objectClass=user)" givenName
```

- join AD

```
domainjoin-cli join secure.local domain-bind
```

- bug fix in ubuntu 14.04 when joining to a domain

```
killall aptd
apt-get install packagekit adcli
```

## Nagios

- plugins: `/usr/local/nagios/plugins/`
- check syntax `/usr/local/nagios/bin/nagios -v /etc/nagios.cfg`

```
 /usr/local/nagios/libexec/check_by_ssh -H [host] -l nagios -C'/usr/local/nagios/libexec/check_disk -w 15% -c 10% -p /productdb'
```

## PID debug

```
strace -p 4293 -s 80 -o /tmp/debug.php
```

## Hack

```
# cause system not logging bash commands
ln -s /dev/null .bash_history
```

## Security

- likewise

```
/opt/pbis/bin/config --dump
/opt/pbis/bin/get-status
/opt/pbis/bin/find-objects --user USERNAME
```

/etc/pam.d/common-session

```
session [default=1]                     pam_permit.so
session requisite                       pam_deny.so
session required                        pam_permit.so
session optional                        pam_umask.so
session required                        pam_unix.so
session optional                        pam_mount.so
session [success=ok default=ignore]     pam_lsass.so
session optional                        pam_systemd.so
```

/etc/pam.d/common-auth

```
auth    [success=2 default=ignore]      pam_unix.so nullok_secure
auth    [success=1 default=ignore]      pam_lsass.so try_first_pass
auth    requisite                       pam_deny.so
auth    required                        pam_permit.so
auth    optional                        pam_cap.so
auth    optional                        pam_mount.so
```

/opt/pbis/share/pbis.pam-auth-update

```
Name: Likewise
Default: yes
Priority: 250
Conflicts: winbind
Auth-Type: Primary
Auth:
        [success=end default=ignore]    pam_lsass.so try_first_pass
Auth-Initial:
        [success=end default=ignore]    pam_lsass.so
Account-Type: Primary
Account:
        [success=ok new_authtok_reqd=ok default=ignore]         pam_lsass.so unknown_ok
        [success=end new_authtok_reqd=done default=ignore]      pam_lsass.so
Session-Type: Additional
Session:
        sufficient      pam_lsass.so
Password-Type: Primary
Password:
        [success=end default=ignore]    pam_lsass.so use_authtok try_first_pass
Password-Initial:
        [success=end default=ignore]    pam_lsass.so
```

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
# get the descrepency
ntpq -pn | /usr/bin/awk 'BEGIN { offset=1000 } $1 ~ /\*/ { offset=$9 } END { print offset }'
```

### SSH

`ssh -Q cipher` from the client will tell you which schemes your client supports.

`nmap --script ssh2-enum-algos -sV -p <port> <host>` will tell you which schemes your server supports.

```
sudo sshd -T |grep ciphers => ciphers aes256-ctr
add "ciphers aes256-ctr" to "/etc/ssh/sshd_config", restart sshd service
```

### JAVA

install java8 on ubuntu 14.04

```shell
sudo apt-get update && sudo apt-get install oracle-java8-installer
sudo apt-get install oracle-java8-set-default
```

## Contact

Binh Nguyen
