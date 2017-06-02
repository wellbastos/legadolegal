# Palantir: a pedra vidente de Numenor
# 
# Script para inspecao basica da infraestrutura de dominios WLS 10g, 11g e 12c
#
connect(url='t3s://<IP>:<PORTA>')

def checkVM(server):
  print '## JVM'
  print 'Status:', server.getState()
  print 'Info: ', server.getListenAddress(),':',server.getListenPort()
  print 'Saúde: ', server.getHealthState()

def checkJMS(server):
  print '## JMS'
  jmsRuntime = server.getJMSRuntime();
  jmsServers = jmsRuntime.getJMSServers();
  for jmsServer in jmsServers:
    destinations = jmsServer.getDestinations();
    for destination in destinations:
      print jmsRuntime.getName(), destination.getName(), ': ', destination.getState()

def checkMemory(server):
  print '## Memória'
  print('%20s %10s %8s %8s %4s' % ('Servidor','Atual','%','Max','Livre'))
  free    = int(server.getJVMRuntime().getHeapFreeCurrent())/(1024*1024)
  freePct = int(server.getJVMRuntime().getHeapFreePercent())
  current = int(server.getJVMRuntime().getHeapSizeCurrent())/(1024*1024)
  max     = int(server.getJVMRuntime().getHeapSizeMax())/(1024*1024)
  print('%20s %7d MB %5d MB %5d MB %3d%%' % (server.getName(),current,free,max,freePct))

def checkJDBC(server):
  print '## JDBC'
  jdbcServiceRT = server.getJDBCServiceRuntime();
  dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
  if (len(dataSources) > 0):
    for dataSource in dataSources:
      print dataSource.getName(),": ",dataSource.getState()

def checkApps(server):
  domain = domainRuntimeService.getDomainRuntime()
  appRT = domain.getAppRuntimeStateRuntime()
  apps = appRT.getApplicationIds()
  print '## Pacotes'

  for app in apps:
    appState = appRT.getCurrentState(app, serverName)
    print appState, ' ', app

def main():
  servers = domainRuntimeService.getServerRuntimes()
  if (len(servers) > 0):
    for server in servers:
      serverName = server.getName();
      print '**************************************************\n'
      print '##############    ', serverName,    '###############'
      print '**************************************************\n'
      checkVM(server)
      checkJMS(server)
      checkMemory(server)
      checkJDBC(server)
      checkApps(server)
main()
