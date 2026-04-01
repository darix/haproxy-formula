{% from tpldir ~ "/map.jinja" import haproxy with context %}

haproxy.install:
  pkg.installed:
    - pkgs:
      {%- if salt['pillar.get']('haproxy:minimum_version', "") != "" %}
      - {{ haproxy.package }}: '>={{ salt['pillar.get']('haproxy:minimum_version', "") }}'
      {%- else %}
      - {{ haproxy.package }}
      {%- endif %}
      {% for package in salt['pillar.get']('haproxy:extra_packages', []) %}
      - {{ package }}
      {%- endfor %}
{% if salt['pillar.get']('haproxy:require') %}
    - require:
{% for item in salt['pillar.get']('haproxy:require') %}
      - {{ item }}
{% endfor %}
{% endif %}
