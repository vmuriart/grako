from __future__ import absolute_import, unicode_literals

from grako import graken, Parser

KEYWORDS = {'ABS',
            'ALL',
            'ALLOCATE',
            'ALTER',
            'AND',
            'ANY',
            'ARE',
            'ARRAY',
            'ARRAY_AGG',
            'ARRAY_MAX_CARDINALITY',
            'AS',
            'ASENSITIVE',
            'ASYMMETRIC',
            'AT',
            'ATOMIC',
            'AUTHORIZATION',
            'AVG',
            'BEGIN',
            'BEGIN_FRAME',
            'BEGIN_PARTITION',
            'BETWEEN',
            'BIGINT',
            'BINARY',
            'BLOB',
            'BOOLEAN',
            'BOTH',
            'BY',
            'CALL',
            'CALLED',
            'CARDINALITY',
            'CASCADED',
            'CASE',
            'CAST',
            'CEIL',
            'CEILING',
            'CHAR',
            'CHARACTER',
            'CHARACTER_LENGTH',
            'CHAR_LENGTH',
            'CHECK',
            'CLOB',
            'CLOSE',
            'COALESCE',
            'COLLATE',
            'COLLECT',
            'COLUMN',
            'COMMIT',
            'CONDITION',
            'CONNECT',
            'CONSTRAINT',
            'CONTAINS',
            'CONVERT',
            'CORR',
            'CORRESPONDING',
            'COUNT',
            'COVAR_POP',
            'COVAR_SAMP',
            'CREATE',
            'CROSS',
            'CUBE',
            'CUME_DIST',
            'CURRENT',
            'CURRENT_CATALOG',
            'CURRENT_DATE',
            'CURRENT_DEFAULT_TRANSFORM_GROUP',
            'CURRENT_PATH',
            'CURRENT_ROLE',
            'CURRENT_ROW',
            'CURRENT_SCHEMA',
            'CURRENT_TIME',
            'CURRENT_TIMESTAMP',
            'CURRENT_TRANSFORM_GROUP_FOR_TYPE',
            'CURRENT_USER',
            'CURSOR',
            'CYCLE',
            'DATE',
            'DAY',
            'DEALLOCATE',
            'DEC',
            'DECIMAL',
            'DECLARE',
            'DECODE',
            'DEFAULT',
            'DELETE',
            'DENSE_RANK',
            'DEREF',
            'DESCRIBE',
            'DETERMINISTIC',
            'DISCONNECT',
            'DISTINCT',
            'DOUBLE',
            'DROP',
            'DYNAMIC',
            'EACH',
            'ELEMENT',
            'ELSE',
            'END',
            'END_EXEC',
            'END_FRAME',
            'END_PARTITION',
            'EQUALS',
            'ESCAPE',
            'EVERY',
            'EXCEPT',
            'EXEC',
            'EXECUTE',
            'EXISTS',
            'EXP',
            'EXTERNAL',
            'EXTRACT',
            'FALSE',
            'FETCH',
            'FILTER',
            'FIRST_VALUE',
            'FLOAT',
            'FLOOR',
            'FOR',
            'FOREIGN',
            'FRAME_ROW',
            'FREE',
            'FROM',
            'FULL',
            'FUNCTION',
            'FUSION',
            'GET',
            'GLOBAL',
            'GRANT',
            'GROUP',
            'GROUPING',
            'GROUPS',
            'HAVING',
            'HOLD',
            'HOUR',
            'IDENTITY',
            'IN',
            'INDICATOR',
            'INNER',
            'INOUT',
            'INSENSITIVE',
            'INSERT',
            'INT',
            'INTEGER',
            'INTERSECT',
            'INTERSECTION',
            'INTERVAL',
            'INTO',
            'IS',
            'JOIN',
            'LAG',
            'LANGUAGE',
            'LARGE',
            'LAST_VALUE',
            'LATERAL',
            'LEAD',
            'LEADING',
            'LEFT',
            'LIKE',
            'LIKE_REGEX',
            'LN',
            'LOCAL',
            'LOCALTIME',
            'LOCALTIMESTAMP',
            'LOWER',
            'MATCH',
            'MAX',
            'MEMBER',
            'MERGE',
            'METHOD',
            'MIN',
            'MINUTE',
            'MOD',
            'MODIFIES',
            'MODULE',
            'MONTH',
            'MULTISET',
            'NATIONAL',
            'NATURAL',
            'NCHAR',
            'NCLOB',
            'NEW',
            'NO',
            'NONE',
            'NORMALIZE',
            'NOT',
            'NTH_VALUE',
            'NTILE',
            'NULL',
            'NULLIF',
            'NUMERIC',
            'OCCURRENCES_REGEX',
            'OCTET_LENGTH',
            'OF',
            'OFFSET',
            'OLD',
            'ON',
            'ONLY',
            'OPEN',
            'OR',
            'ORDER',
            'OUT',
            'OUTER',
            'OVER',
            'OVERLAPS',
            'OVERLAY',
            'PARAMETER',
            'PARTITION',
            'PERCENT',
            'PERCENTILE_CONT',
            'PERCENTILE_DISC',
            'PERCENT_RANK',
            'PERIOD',
            'PORTION',
            'POSITION',
            'POSITION_REGEX',
            'POWER',
            'PRECEDES',
            'PRECISION',
            'PREPARE',
            'PRIMARY',
            'PROCEDURE',
            'RANGE',
            'RANK',
            'READS',
            'REAL',
            'RECURSIVE',
            'REF',
            'REFERENCES',
            'REFERENCING',
            'REGR_AVGX',
            'REGR_AVGY',
            'REGR_COUNT',
            'REGR_INTERCEPT',
            'REGR_R2',
            'REGR_SLOPE',
            'REGR_SXX',
            'REGR_SXY',
            'REGR_SYY',
            'RELEASE',
            'RESULT',
            'RETURN',
            'RETURNS',
            'REVOKE',
            'RIGHT',
            'ROLLBACK',
            'ROLLUP',
            'ROW',
            'ROWS',
            'ROW_NUMBER',
            'SAVEPOINT',
            'SCOPE',
            'SCROLL',
            'SEARCH',
            'SECOND',
            'SELECT',
            'SENSITIVE',
            'SESSION_USER',
            'SET',
            'SIMILAR',
            'SMALLINT',
            'SOME',
            'SPECIFIC',
            'SPECIFICTYPE',
            'SQL',
            'SQLEXCEPTION',
            'SQLSTATE',
            'SQLWARNING',
            'SQRT',
            'START',
            'STATIC',
            'STDDEV_POP',
            'STDDEV_SAMP',
            'SUBMULTISET',
            'SUBSTRING',
            'SUBSTRING_REGEX',
            'SUCCEEDS',
            'SUM',
            'SYMMETRIC',
            'SYSTEM',
            'SYSTEM_TIME',
            'SYSTEM_USER',
            'TABLE',
            'TABLESAMPLE',
            'THEN',
            'TIME',
            'TIMESTAMP',
            'TIMEZONE_HOUR',
            'TIMEZONE_MINUTE',
            'TO',
            'TRAILING',
            'TRANSLATE',
            'TRANSLATE_REGEX',
            'TRANSLATION',
            'TREAT',
            'TRIGGER',
            'TRIM',
            'TRIM_ARRAY',
            'TRUE',
            'TRUNCATE',
            'UESCAPE',
            'UNION',
            'UNIQUE',
            'UNKNOWN',
            'UNNEST',
            'UPDATE',
            'UPPER',
            'USER',
            'USING',
            'VALUE_OF',
            'VARBINARY',
            'VARCHAR',
            'VARYING',
            'VAR_POP',
            'VAR_SAMP',
            'VERSIONING',
            'WHEN',
            'WHENEVER',
            'WHERE',
            'WIDTH_BUCKET',
            'WINDOW',
            'WITH',
            'WITHIN',
            'WITHOUT',
            'YEAR',
            }


class SqlParser(Parser):
    def __init__(self):
        super(SqlParser, self).__init__(eol_comments_re='--.*?$',
                                        keywords=KEYWORDS)

    @graken
    def _integer_(self):
        self._pattern(r'\d+')

    @graken
    def _integer_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._integer_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _regular_identifier_(self):
        token = self._pattern(r'[a-z]\w*')
        self._check_name(token)

    @graken
    def _unquoted_interval_str_(self):
        with self._choice():
            with self._option():
                self._integer_()
                with self._optional():
                    self._token('-')
                    self._integer_()
            with self._option():
                self._integer_()
                with self._optional():
                    self._integer_()
                    with self._optional():
                        self._token(':')
                        self._integer_()
                        with self._optional():
                            self._token(':')
                            self._proper_decimal_()
            with self._option():
                self._integer_()
                with self._optional():
                    self._token(':')
                    self._integer_()
                    with self._optional():
                        self._token(':')
                        self._proper_decimal_()
            with self._option():
                self._integer_()
                with self._optional():
                    self._token(':')
                    self._proper_decimal_()
            with self._option():
                self._proper_decimal_()
            self._error('no available options')

    @graken
    def _proper_decimal_(self):
        self._integer_()
        with self._optional():
            self._token('.')
            with self._optional():
                self._integer_()

    @graken
    def _sign_(self):
        with self._choice():
            with self._option():
                self._token('+')
            with self._option():
                self._token('-')
            self._error('expecting one of: + -')

    @graken
    def _name_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._qualified_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _identifier_(self):
        with self._choice():
            with self._option():
                self._regular_identifier_()
            with self._option():
                self._token('"')
                self._pattern(r'(""|[^"\n])+')
                self._token('"')
            self._error('expecting one of: "')

    @graken
    def _qualified_name_(self):
        with self._optional():
            self._token('MODULE')
            self._token('.')

        def sep0():
            self._token('.')

        def block0():
            self._identifier_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _parameter_name_(self):
        self._token(':')
        self._identifier_()

    @graken
    def _data_type_(self):
        with self._choice():
            with self._option():
                self._token('CHARACTER')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('CHAR')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('NUMERIC')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('DECIMAL')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('DEC')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('SMALLINT')
            with self._option():
                self._token('INTEGER')
            with self._option():
                self._token('INT')
            with self._option():
                self._token('BIGINT')
            with self._option():
                self._token('FLOAT')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('REAL')
            with self._option():
                self._token('DOUBLE')
                self._token('PRECISION')
            with self._option():
                self._token('BOOLEAN')
            with self._option():
                self._token('DATE')
            with self._option():
                self._token('TIME')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('TIMESTAMP')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('INTERVAL')
                self._interval_qualifier_()
            self._error('expecting one of: BIGINT BOOLEAN CHAR CHARACTER DATE'
                        ' DEC DECIMAL DOUBLE FLOAT INT INTEGER NUMERIC REAL'
                        ' SMALLINT TIME TIMESTAMP')

    @graken
    def _value_expr_primary_(self):
        with self._choice():
            with self._option():
                self._token('DECODE')
                self._value_expr_list_()
            with self._option():
                self._rank_function_type_()
                self._token('(')
                self._token(')')
                self._token('OVER')
                self._window_spec_()
            with self._option():
                self._token('ROW_NUMBER')
                self._token('(')
                self._token(')')
                self._token('OVER')
                self._window_spec_()
            with self._option():
                self._aggregate_function_()
                with self._optional():
                    self._token('OVER')
                    self._window_spec_()
            with self._option():
                self._subquery_()
            with self._option():
                self._token('NULLIF')
                self._value_expr_list_()
            with self._option():
                self._token('LENGTH')
                self._value_expr_list_()
            with self._option():
                self._token('COALESCE')
                self._value_expr_list_()
            with self._option():
                self._token('SUBSTR')
                self._value_expr_list_()
            with self._option():
                self._token('REGEXP_SUBSTR')
                self._value_expr_list_()
            with self._option():
                self._token('REGEXP_REPLACE')
                self._value_expr_list_()
            with self._option():
                self._case_expr_()
            with self._option():
                self._token('CAST')
                self._token('(')
                self._result_()
                self._token('AS')
                self._data_type_()
                self._token(')')
            with self._option():
                self._token('TREAT')
                self._token('(')
                self._value_expr_()
                self._token('AS')
                self._qualified_name_()
                self._token(')')
            with self._option():
                self._proper_decimal_()
                with self._optional():
                    self._token('E')
                    with self._optional():
                        self._sign_()
                    self._integer_()
            with self._option():
                self._token('.')
                self._integer_()
                with self._optional():
                    self._token('E')
                    with self._optional():
                        self._sign_()
                    self._integer_()
            with self._option():
                self._token("'")
                self._pattern(r"(''|[^'\n])*")
                self._token("'")
            with self._option():
                self._token('DATE')
                self._token("'")
                self._integer_()
                self._token('-')
                self._integer_()
                self._token('-')
                self._integer_()
                self._token("'")
            with self._option():
                self._token('TIME')
                self._token("'")
                self._integer_()
                self._token(':')
                self._integer_()
                self._token(':')
                self._proper_decimal_()
                self._token("'")
            with self._option():
                self._token('TIMESTAMP')
                self._token("'")
                self._integer_()
                self._token('-')
                self._integer_()
                self._token('-')
                self._integer_()
                self._integer_()
                self._token(':')
                self._integer_()
                self._token(':')
                self._proper_decimal_()
                self._token("'")
            with self._option():
                self._token('INTERVAL')
                with self._optional():
                    self._sign_()
                self._token("'")
                with self._optional():
                    self._sign_()
                self._unquoted_interval_str_()
                self._token("'")
                self._interval_qualifier_()
            with self._option():
                self._token('TRUE')
            with self._option():
                self._token('FALSE')
            with self._option():
                self._token('UNKNOWN')
            with self._option():
                self._parameter_name_()
            with self._option():
                self._token('?')
            with self._option():
                self._token('CURRENT_ROLE')
            with self._option():
                self._token('CURRENT_USER')
            with self._option():
                self._token('SESSION_USER')
            with self._option():
                self._token('SYSTEM_USER')
            with self._option():
                self._token('USER')
            with self._option():
                self._token('VALUE')
            with self._option():
                self._qualified_name_()
            self._error("expecting one of: ' ? CURRENT_ROLE CURRENT_USER FALSE"
                        " SESSION_USER SYSTEM_USER TRUE UNKNOWN USER VALUE")

    @graken
    def _rank_function_type_(self):
        with self._choice():
            with self._option():
                self._token('RANK')
            with self._option():
                self._token('DENSE_RANK')
            with self._option():
                self._token('PERCENT_RANK')
            with self._option():
                self._token('CUME_DIST')
            self._error('expecting one of: CUME_DIST DENSE_RANK PERCENT_RANK'
                        ' RANK')

    @graken
    def _case_expr_(self):
        with self._choice():
            with self._option():
                self._token('CASE')
                self._value_expr_()

                def block0():
                    self._simple_when_clause_()

                self._positive_closure(block0)
                with self._optional():
                    self._else_clause_()
                self._token('END')
            with self._option():
                self._token('CASE')

                def block1():
                    self._searched_when_clause_()

                self._positive_closure(block1)
                with self._optional():
                    self._else_clause_()
                self._token('END')
            self._error('no available options')

    @graken
    def _simple_when_clause_(self):
        self._token('WHEN')
        self._when_operand_list_()
        self._token('THEN')
        self._result_()

    @graken
    def _searched_when_clause_(self):
        self._token('WHEN')
        self._boolean_value_expr_()
        self._token('THEN')
        self._result_()

    @graken
    def _else_clause_(self):
        self._token('ELSE')
        self._result_()

    @graken
    def _when_operand_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._when_operand_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _when_operand_(self):
        with self._choice():
            with self._option():
                self._part_predicate_()
            with self._option():
                self._value_expr_()
            self._error('no available options')

    @graken
    def _part_predicate_(self):
        with self._choice():
            with self._option():
                self._comp_op_()
                self._value_expr_()
            with self._option():
                self._comp_op_()
                self._quantifier_()
                self._subquery_()
            with self._option():
                self._token('OVERLAPS')
                self._value_expr_()
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('NULL')
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('NORMALIZED')
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('DISTINCT')
                self._token('FROM')
                self._value_expr_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('IN')
                self._in_predicate_value_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('LIKE')
                self._value_expr_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('BETWEEN')
                self._value_expr_()
                self._token('AND')
                self._value_expr_()
            self._error('expecting one of: IS')

    @graken
    def _result_(self):
        with self._choice():
            with self._option():
                self._token('NULL')
            with self._option():
                self._value_expr_()
            self._error('expecting one of: NULL')

    @graken
    def _value_expr_(self):
        with self._choice():
            with self._option():
                with self._optional():
                    self._value_expr_()
                    self._ops_()
                with self._optional():
                    self._sign_()
                self._primary_()
            with self._option():
                self._boolean_value_expr_()
            self._error('no available options')

    @graken
    def _value_expr_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._value_expr_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _ops_(self):
        with self._choice():
            with self._option():
                self._sign_()
            with self._option():
                self._token('*')
            with self._option():
                self._token('/')
            with self._option():
                self._token('||')
            self._error('expecting one of: * / ||')

    @graken
    def _primary_(self):
        with self._choice():
            with self._option():
                self._token('POSITION')
                self._token('(')
                self._value_expr_()
                self._token('IN')
                self._value_expr_()
                self._token(')')
            with self._option():
                self._token('EXTRACT')
                self._token('(')
                self._extract_field_()
                self._token('FROM')
                self._value_expr_()
                self._token(')')
            with self._option():
                self._token('CHAR_LENGTH')
                self._value_expr_list_()
            with self._option():
                self._token('CHARACTER_LENGTH')
                self._value_expr_list_()
            with self._option():
                self._token('OCTET_LENGTH')
                self._value_expr_list_()
            with self._option():
                self._token('ABS')
                self._value_expr_list_()
            with self._option():
                self._token('MOD')
                self._value_expr_list_()
            with self._option():
                self._token('LN')
                self._value_expr_list_()
            with self._option():
                self._token('EXP')
                self._value_expr_list_()
            with self._option():
                self._token('POWER')
                self._value_expr_list_()
            with self._option():
                self._token('SQRT')
                self._value_expr_list_()
            with self._option():
                self._token('FLOOR')
                self._value_expr_list_()
            with self._option():
                self._token('CEIL')
                self._value_expr_list_()
            with self._option():
                self._token('CEILING')
                self._value_expr_list_()
            with self._option():
                self._token('WIDTH_BUCKET')
                self._value_expr_list_()
            with self._option():
                self._token('SUBSTRING')
                self._token('(')
                self._value_expr_()
                self._token('FROM')
                self._value_expr_()
                with self._optional():
                    self._token('FOR')
                    self._value_expr_()
                self._token(')')
            with self._option():
                self._token('UPPER')
                self._value_expr_list_()
            with self._option():
                self._token('LOWER')
                self._value_expr_list_()
            with self._option():
                self._token('TRIM')
                self._value_expr_list_()
            with self._option():
                self._token('NORMALIZE')
                self._value_expr_list_()
            with self._option():
                self._token('CURRENT_DATE')
            with self._option():
                self._token('CURRENT_TIME')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('CURRENT_TIMESTAMP')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('LOCALTIME')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._token('LOCALTIMESTAMP')
                with self._optional():
                    self._integer_list_()
            with self._option():
                self._value_expr_list_()
            with self._option():
                self._value_expr_primary_()
            self._error('expecting one of: CURRENT_DATE CURRENT_TIME'
                        ' CURRENT_TIMESTAMP LOCALTIME LOCALTIMESTAMP')

    @graken
    def _extract_field_(self):
        with self._choice():
            with self._option():
                self._datetime_field_()
            with self._option():
                self._token('TIMEZONE_HOUR')
            with self._option():
                self._token('TIMEZONE_MINUTE')
            self._error('expecting one of: TIMEZONE_HOUR TIMEZONE_MINUTE')

    @graken
    def _boolean_value_expr_(self):
        with self._optional():
            self._token('NOT')
        self._boolean_primary_()
        with self._optional():
            def block0():
                self._and_or_()
                with self._optional():
                    self._token('NOT')
                self._boolean_primary_()

            self._positive_closure(block0)

    @graken
    def _and_or_(self):
        with self._choice():
            with self._option():
                self._token('AND')
            with self._option():
                self._token('OR')
            self._error('expecting one of: AND OR')

    @graken
    def _boolean_primary_(self):
        with self._choice():
            with self._option():
                self._value_expr_()
                self._part_predicate_()
            with self._option():
                self._token('EXISTS')
                self._subquery_()
            with self._option():
                self._token('UNIQUE')
                self._subquery_()
            with self._option():
                self._token('(')
                self._boolean_value_expr_()
                self._token(')')
            with self._option():
                self._value_expr_primary_()
            self._error('no available options')

    @graken
    def _all_distinct_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
            with self._option():
                self._token('DISTINCT')
            self._error('expecting one of: ALL DISTINCT')

    @graken
    def _table_expr_(self):
        self._from_clause_()
        with self._optional():
            self._where_clause_()
        with self._optional():
            self._group_by_clause_()
        with self._optional():
            self._having_clause_()
        with self._optional():
            self._connect_clause_()

    @graken
    def _connect_clause_(self):
        self._token('CONNECT')
        self._token('BY')
        self._boolean_value_expr_()

    @graken
    def _from_clause_(self):
        self._token('FROM')
        self._table_reference_list_()

    @graken
    def _table_reference_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._table_reference_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _table_reference_(self):
        with self._choice():
            with self._option():
                self._joined_table_()
            with self._option():
                self._table_primary_()
            self._error('no available options')

    @graken
    def _table_primary_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._joined_table_()
                self._token(')')
            with self._option():
                self._subquery_()
                with self._optional():
                    self._as_clause_()
            with self._option():
                self._qualified_name_()
                with self._optional():
                    self._as_clause_()
            self._error('no available options')

    @graken
    def _joined_table_(self):
        with self._choice():
            with self._option():
                self._table_reference_()
                self._token('CROSS')
                self._token('JOIN')
                self._table_primary_()
            with self._option():
                self._table_reference_()
                with self._optional():
                    self._join_type_()
                self._token('JOIN')
                self._table_reference_()
                self._token('ON')
                self._boolean_value_expr_()
            with self._option():
                self._table_reference_()
                self._token('NATURAL')
                with self._optional():
                    self._join_type_()
                self._token('JOIN')
                self._table_primary_()
            self._error('no available options')

    @graken
    def _join_type_(self):
        with self._choice():
            with self._option():
                self._token('INNER')
            with self._option():
                self._outer_join_type_()
                with self._optional():
                    self._token('OUTER')
            self._error('expecting one of: INNER')

    @graken
    def _outer_join_type_(self):
        with self._choice():
            with self._option():
                self._token('LEFT')
            with self._option():
                self._token('RIGHT')
            with self._option():
                self._token('FULL')
            self._error('expecting one of: FULL LEFT RIGHT')

    @graken
    def _where_clause_(self):
        self._token('WHERE')
        self._boolean_value_expr_()

    @graken
    def _group_by_clause_(self):
        self._token('GROUP')
        self._token('BY')
        with self._optional():
            self._all_distinct_()
        self._grouping_element_list_()

    @graken
    def _grouping_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._grouping_set_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _grouping_set_(self):
        with self._choice():
            with self._option():
                self._token('(')
                with self._optional():
                    self._name_list_()
                self._token(')')
            with self._option():
                self._qualified_name_()
            self._error('expecting one of: (')

    @graken
    def _having_clause_(self):
        self._token('HAVING')
        self._boolean_value_expr_()

    @graken
    def _window_spec_(self):
        self._token('(')
        with self._optional():
            self._partition_clause_()
        with self._optional():
            self._order_by_clause_()
        self._token(')')

    @graken
    def _partition_clause_(self):
        self._token('PARTITION')
        self._token('BY')
        self._name_list_()

    @graken
    def _select_list_(self):
        with self._choice():
            with self._option():
                self._token('*')
            with self._option():
                def sep0():
                    self._token(',')

                def block0():
                    self._select_sublist_()

                self._positive_closure(block0, prefix=sep0)
            self._error('expecting one of: *')

    @graken
    def _select_sublist_(self):
        with self._choice():
            with self._option():
                self._value_expr_()
                with self._optional():
                    self._as_clause_()
            with self._option():
                self._qualified_name_()
                self._token('.')
                self._token('*')
            self._error('no available options')

    @graken
    def _as_clause_(self):
        with self._optional():
            self._token('AS')
        self._identifier_()

    @graken
    def _query_expr_(self):
        with self._optional():
            self._token('WITH')
            self._with_list_()
        self._query_expr_body_()

    @graken
    def _with_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._identifier_()
            self._token('AS')
            self._subquery_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _query_expr_body_(self):
        self._query_primary_()
        with self._optional():
            def block0():
                self._union_except_()
                with self._optional():
                    self._all_distinct_()
                self._query_primary_()

            self._positive_closure(block0)

    @graken
    def _union_except_(self):
        with self._choice():
            with self._option():
                self._token('UNION')
            with self._option():
                self._token('EXCEPT')
            with self._option():
                self._token('INTERSECT')
            self._error('expecting one of: EXCEPT INTERSECT UNION')

    @graken
    def _query_primary_(self):
        with self._choice():
            with self._option():
                self._token('SELECT')
                with self._optional():
                    self._all_distinct_()
                self._select_list_()
                self._table_expr_()
            with self._option():
                self._token('(')
                self._query_expr_body_()
                self._token(')')
            self._error('no available options')

    @graken
    def _subquery_(self):
        self._token('(')
        self._query_expr_()
        self._token(')')

    @graken
    def _comp_op_(self):
        with self._choice():
            with self._option():
                self._token('<=')
            with self._option():
                self._token('>=')
            with self._option():
                self._token('<>')
            with self._option():
                self._token('=')
            with self._option():
                self._token('!=')
            with self._option():
                self._token('<')
            with self._option():
                self._token('>')
            self._error('expecting one of: != < <= <> = > >=')

    @graken
    def _in_predicate_value_(self):
        with self._choice():
            with self._option():
                self._subquery_()
            with self._option():
                self._value_expr_list_()
            self._error('no available options')

    @graken
    def _quantifier_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
            with self._option():
                self._token('SOME')
            with self._option():
                self._token('ANY')
            self._error('expecting one of: ALL ANY SOME')

    @graken
    def _interval_qualifier_(self):
        self._datetime_field_()
        with self._optional():
            self._integer_list_()
        with self._optional():
            self._token('TO')
            self._datetime_field_()
            with self._optional():
                self._integer_list_()

    @graken
    def _datetime_field_(self):
        with self._choice():
            with self._option():
                self._token('YEAR')
            with self._option():
                self._token('MONTH')
            with self._option():
                self._token('DAY')
            with self._option():
                self._token('HOUR')
            with self._option():
                self._token('MINUTE')
            with self._option():
                self._token('SECOND')
            self._error('expecting one of: DAY HOUR MINUTE MONTH SECOND YEAR')

    @graken
    def _aggregate_function_(self):
        with self._choice():
            with self._option():
                self._token('COUNT')
                self._token('(')
                self._token('*')
                self._token(')')
                with self._optional():
                    self._filter_clause_()
            with self._option():
                self._computational_operation_()
                self._token('(')
                with self._optional():
                    self._all_distinct_()
                self._value_expr_()
                self._token(')')
                with self._optional():
                    self._filter_clause_()
            self._error('expecting one of: COUNT')

    @graken
    def _computational_operation_(self):
        with self._choice():
            with self._option():
                self._token('AVG')
            with self._option():
                self._token('MAX')
            with self._option():
                self._token('MIN')
            with self._option():
                self._token('SUM')
            with self._option():
                self._token('EVERY')
            with self._option():
                self._token('ANY')
            with self._option():
                self._token('LEAD')
            with self._option():
                self._token('LAG')
            with self._option():
                self._token('COUNT')
            with self._option():
                self._token('STDDEV_POP')
            with self._option():
                self._token('STDDEV_SAMP')
            with self._option():
                self._token('INTERSECTION')
            self._error('expecting one of: ANY AVG COUNT EVERY INTERSECTION'
                        ' LAG LEAD MAX MIN STDDEV_POP STDDEV_SAMP SUM')

    @graken
    def _filter_clause_(self):
        self._token('FILTER')
        self._token('(')
        self._where_clause_()
        self._token(')')

    @graken
    def _sort_spec_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._sort_spec_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _sort_spec_(self):
        self._value_expr_()
        with self._optional():
            self._ordering_spec_()
        with self._optional():
            self._null_ordering_()

    @graken
    def _ordering_spec_(self):
        with self._choice():
            with self._option():
                self._token('ASC')
            with self._option():
                self._token('DESC')
            self._error('expecting one of: ASC DESC')

    @graken
    def _null_ordering_(self):
        with self._choice():
            with self._option():
                self._token('NULLS')
                self._token('FIRST')
            with self._option():
                self._token('NULLS')
                self._token('LAST')
            self._error('expecting one of: NULLS')

    @graken
    def _cursor_spec_(self):
        self._query_expr_()
        with self._optional():
            self._order_by_clause_()

    @graken
    def _order_by_clause_(self):
        self._token('ORDER')
        self._token('BY')
        self._sort_spec_list_()

    @graken
    def _start_(self):
        self._cursor_spec_()
        self._check_eof()
