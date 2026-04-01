{% from tpldir ~ "/map.jinja" import haproxy with context %}

haproxy.install:
  pkg.installed:
    - pkgs:
      {%- if salt['pillar.get']('haproxy:minimum_version', "") != "" %}
      - {{ haproxy.package }}: '>={{ salt['pillar.get']('haproxy:minimum_version', "") }}'
      {%- else %}
      - {{ haproxy.package }}
      {%- endif %}
      - hatop
      - monitoring-plugins-haproxy
{% if salt['pillar.get']('haproxy:require') %}
    - require:
{% for item in salt['pillar.get']('haproxy:require') %}
      - {{ item }}
{% endfor %}
{% endif %}
