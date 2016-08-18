"""
The MIT License (MIT)

Copyright (c) 2016 Formstack, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pymysql

from checks import AgentCheck
from contextlib import closing, contextmanager


class GearmanMySQLCheck(AgentCheck):
    SERVICE_CHECK_NAME = 'gearman_mysql.can_connect'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        collected_metrics = None

        host, user, password, database, table, port = \
            self._get_config(instance)

        if (not host or not user):
            raise Exception("mysql_host and mysql_user are needed.")

        with self._connect(host, user, password, port, database) as db:
            try:
                collected_metrics = self._collect_queue_metrics(db)
            except Exception:
                self.log.exception("error!")

        for collected_metric in collected_metrics:
            gauge_tags = [
                'queue:%s' % collected_metric['function_name'],
                'priority:%s' % str(collected_metric['priority']),
            ]
            self.gauge('gearman_mysql.queue',
                       collected_metric['cnt'],
                       gauge_tags)

    def _get_config(self, instance):
        self.host = instance.get('mysql_host', '')
        self.user = instance.get('mysql_user', '')
        self.password = instance.get('mysql_password', '')
        self.database = instance.get('mysql_database', 'gearmand')
        self.table = instance.get('mysql_table', 'gearman_queue')
        self.port = instance.get('mysql_port', 3306)

        return (self.host, self.user, self.password, self.database,
                self.table, self.port)

    @contextmanager
    def _connect(self, host, user, password, port, database):

        self.service_check_tags = [
            'server:%s' % host,
            'port:%s' % port
        ]

        db = None

        try:
            db = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=password,
                db=database,
            )
            self.log.debug("Connected to MySQL")
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK,
                               tags=self.service_check_tags)
            yield db
        except Exception:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                               tags=self.service_check_tags)
            raise
        finally:
            if db:
                db.close()

    def _collect_queue_metrics(self, db):

        with closing(db.cursor(pymysql.cursors.DictCursor)) as cursor:
            cursor.execute("SELECT function_name, priority, count(*) AS cnt "
                           "FROM " + self.table + " "
                           "GROUP BY function_name, priority")
            results = cursor.fetchall()

        return results
