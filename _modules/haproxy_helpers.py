class ServerEntries:
  def __init__(self, server_name, server_entry):
    self.server_name = server_name
    self.server_entry = server_entry

    self.lines = []

  def entries(self):
    self.build_lines()
    return self.lines

  def construct_line(self, name, host, loop_index=None):
    server = self.server_entry
    line_elements = []
    line_elements.append('server')
    line_elements.append(name)

    if 'port' in server:
      line_elements.append('{host}:{port}'.format(host=host, port=server['port']))
    else:
      line_elements.append(host)

    if 'maxconn' in server:
      line_elements.append('maxconn {maxconn}'.format(maxconn=server['maxconn']))

    if 'check' in server:
      line_elements.append(server['check'])

    if 'extra' in server:
      line_elements.append(server['extra'])

    if not('extra' in server and 'weight' in server['extra']):

      if 'mine_max_weight' in server:
        weight = server['mine_max_weight']

        if 'mine_scale_weight' in server and server['mine_scale_weight'] and loop_index:
          weight -= loop_index
        line_elements.append('weight {weight}'.format(weight=weight))

        if 'mine_setbackup' in server and server['mine_setbackup']:
          if not('extra' in server and 'backup' in server['extra']):
            if weight < server['mine_max_weight']:
              line_elements.append('backup')

    return ' '.join(line_elements)

  def handle_mine_entry(self, address, name, loop_index):
    minion_name = '{name}{index}'.format(name=name, index=loop_index)
    line = self.construct_line(minion_name, address, loop_index)
    self.lines.append(line)

  def build_lines(self):
    server = self.server_entry
    name = server.get('name', self.server_name)
    line = None
    if 'host' in server:
      line = self.construct_line(name, server['host'])
      self.lines.append(line)
    else:
      if 'mine_target' in server and 'mine_functions' in server:

        mine_target    = server['mine_target']
        mine_functions = server['mine_functions']

        loop_index = 1

        hosts = __salt__['mine.get'](mine_target, mine_functions, tgt_type='compound')

        for minion_id, entry in self.dictsort(hosts).items():

          if type(entry) == list:
            for address in entry:
              self.handle_mine_entry(address, name, loop_index)
              loop_index += 1

          else:
            self.handle_mine_entry(entry, name, loop_index)
            loop_index += 1

  def dictsort(self, unsorted_dict):
    return dict(sorted(unsorted_dict.items(), key=lambda item: item[0]))

def server_entries(server_name='', server_entry=None):
  lines = []

  if not(server_entry):
    server_name="pg-mine"
    server_entry={
      'mine_target':'N@lxc or N@pg',
      'mine_functions': 'fqdn',
      'port': 15432,
      'mine_setbackup': True,
      'mine_scale_weight': True,
      'mine_max_weight': 90,
      'extra': "weight 123",
    }

  return ServerEntries(server_name, server_entry).entries()