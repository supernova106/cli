# All things sensu

- install gem

```
sudo /opt/sensu/embedded/bin/gem install sensu-plugins-influxdb -v 1.2.0
```

- verify gem install

```
/opt/sensu/embedded/bin/irb
/opt/sensu/embedded/lib/ruby/gems/2.4.0/gems/rb-readline-0.5.3/lib/rbreadline.rb:13: warning: constant ::Fixnum is deprecated
irb(main):001:0> require 'influxdb'
=> true
irb(main):002:0>
```