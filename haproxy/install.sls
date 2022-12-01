{% from tpldir ~ "/map.jinja" import haproxy with context %}

haproxy.install:
  pkg.installed:
    - names:
      - {{ haproxy.package }}
      - hatop
      - monitoring-plugins-haproxy
{% if salt['pillar.get']('haproxy:require') %}
    - require:
{% for item in salt['pillar.get']('haproxy:require') %}
      - {{ item }}
{% endfor %}
{% endif %}
