#!/bin/bash

$SCRIPTDIR=$PWD
$LOGDIR=$1

echo "### REPORT GEMFIRE -- SERVIDOR $(hostname -a)"

# validando que há portas no ar (server port e port do locator)
[[ $(for x in $(ps -ef | grep '\-Dgemfire' | egrep "(LocatorLauncher|ServerLauncher)" | egrep -o "\-\-(server\-)*port\=[0-9]+" | cut -d\= -f2);do netstat -nap | awk '{print $4}' | egrep "[0-9]\:${x}" | uniq;done | wc -l) -eq 2 ]] && echo "Portas estão no ar" || echo "Portas estão down, favor verificar"
echo ""
echo "## Informações mínimas do Locator"
echo ""
systemctl status locator | egrep "(Active|PID)" | sed -e 's/^[[:space:]]*//g'

echo ""
echo "## Informações mínimas do Gemfire Server"
echo ""
systemctl status gemfire | egrep "(Active|PID)" | sed -e 's/^[[:space:]]*//g'

LOG_LOCATOR=${LOGDIR}/locator/locator.log
LOG_GEMFIRE=${LOGDIR}/server/logs/server.log

echo ""
echo "## Últimos 10 erros nos logs do Locator"
echo ""
[[ -e $LOG_LOCATOR ]] && echo $LOG_GEMFIRE && egrep -v "(\[info|^$)" $LOG_LOCATOR | tail -10

echo ""
echo "## Últimos 10 erros no log do Gemfire"
echo ""
[[ -e $LOG_GEMFIRE ]] && echo $LOG_GEMFIRE && egrep -v "(\[info|^$)" $LOG_GEMFIRE | tail -10


echo ""
echo "## Iniciando validacoes via GFSH"
gfsh run --file=${SCRIPTDIR}/gemfire_check.gfsh
