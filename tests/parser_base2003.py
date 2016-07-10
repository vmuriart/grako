from __future__ import absolute_import, unicode_literals

from grako import graken, Parser

KEYWORDS = {'SELECT',
            'FROM',
            'WHERE',
            }


class SqlParser(Parser):
    def __init__(self):
        super(SqlParser, self).__init__(eol_comments_re='--.*?$',
                                        keywords=KEYWORDS)

    @graken
    def _start_(self):
        self._direct_sql_statement_()
        self._check_eof()

    @graken
    def _letter_(self):
        self._pattern(r'[a-z]')

    @graken
    def _integer_(self):
        self._pattern(r'\d+')

    @graken
    def _whitespace_(self):
        self._pattern(r'\s+')

    @graken
    def _left_bracket_or_trigraph_(self):
        with self._choice():
            with self._option():
                self._token('[')
            with self._option():
                self._token('??(')
            self._error('expecting one of: ??( [')

    @graken
    def _right_bracket_or_trigraph_(self):
        with self._choice():
            with self._option():
                self._token(']')
            with self._option():
                self._token('??)')
            self._error('expecting one of: ??) ]')

    @graken
    def _regular_identifier_(self):
        token = self._pattern(r'[a-z]\w*')
        self._check_name(token)

    @graken
    def _large_object_length_token_(self):
        self._integer_()
        self._multiplier_()

    @graken
    def _multiplier_(self):
        with self._choice():
            with self._option():
                self._token('K')
            with self._option():
                self._token('M')
            with self._option():
                self._token('G')
            self._error('expecting one of: G K M')

    @graken
    def _delimited_identifier_(self):
        self._token('"')

        def block0():
            self._delimited_identifier_part_()

        self._positive_closure(block0)
        self._token('"')

    @graken
    def _delimited_identifier_part_(self):
        with self._choice():
            with self._option():
                self._letter_()
            with self._option():
                self._token('""')
            self._error('expecting one of: ""')

    @graken
    def _unicode_escape_value_(self):
        with self._choice():
            with self._option():
                self._unicode_4_digit_escape_value_()
            with self._option():
                self._unicode_6_digit_escape_value_()
            with self._option():
                self._unicode_character_escape_value_()
            self._error('no available options')

    @graken
    def _unicode_4_digit_escape_value_(self):
        self._unicode_escape_character_()
        self._hexit_()
        self._hexit_()
        self._hexit_()
        self._hexit_()

    @graken
    def _unicode_6_digit_escape_value_(self):
        self._unicode_escape_character_()
        self._token('+')
        self._hexit_()
        self._hexit_()
        self._hexit_()
        self._hexit_()
        self._hexit_()
        self._hexit_()

    @graken
    def _unicode_character_escape_value_(self):
        self._unicode_escape_character_()
        self._unicode_escape_character_()

    @graken
    def _unicode_escape_character_(self):
        self._token('\\u')

    @graken
    def _separator_(self):
        def block0():
            with self._choice():
                with self._option():
                    self._comment_()
                with self._option():
                    self._whitespace_()
                self._error('no available options')

        self._positive_closure(block0)

    @graken
    def _comment_(self):
        with self._choice():
            with self._option():
                self._simple_comment_()
            with self._option():
                self._bracketed_comment_()
            self._error('no available options')

    @graken
    def _simple_comment_(self):
        self._simple_comment_introducer_()
        with self._optional():
            def block0():
                self._comment_character_()

            self._positive_closure(block0)
        self._newline_()

    @graken
    def _simple_comment_introducer_(self):
        self._token('--')
        with self._optional():
            def block0():
                self._token('-')

            self._positive_closure(block0)

    @graken
    def _bracketed_comment_(self):
        self._token('\\*')
        self._bracketed_comment_contents_()
        self._token('*\\')

    @graken
    def _bracketed_comment_contents_(self):
        with self._optional():
            def block0():
                with self._choice():
                    with self._option():
                        self._comment_character_()
                    with self._option():
                        self._separator_()
                    self._error('no available options')

            self._positive_closure(block0)

    @graken
    def _comment_character_(self):
        with self._choice():
            with self._option():
                self._nonquote_character_()
            with self._option():
                self._token("'")
            self._error("expecting one of: '")

    @graken
    def _newline_(self):
        self._pattern(r'[\r\n]')

    @graken
    def _literal_(self):
        with self._choice():
            with self._option():
                self._signed_numeric_literal_()
            with self._option():
                self._general_literal_()
            self._error('no available options')

    @graken
    def _unsigned_literal_(self):
        with self._choice():
            with self._option():
                self._unsigned_numeric_literal_()
            with self._option():
                self._general_literal_()
            self._error('no available options')

    @graken
    def _general_literal_(self):
        with self._choice():
            with self._option():
                self._character_string_literal_()
            with self._option():
                self._national_character_string_literal_()
            with self._option():
                self._unicode_character_string_literal_()
            with self._option():
                self._binary_string_literal_()
            with self._option():
                self._datetime_literal_()
            with self._option():
                self._interval_literal_()
            with self._option():
                self._boolean_literal_()
            self._error('no available options')

    @graken
    def _character_string_literal_(self):
        with self._optional():
            self._token('_')
            self._character_set_name_()

        def sep0():
            with self._group():
                self._separator_()

        def block0():
            self._token("'")
            with self._optional():
                def block1():
                    self._character_representation_()

                self._positive_closure(block1)
            self._token("'")

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _character_representation_(self):
        with self._choice():
            with self._option():
                self._nonquote_character_()
            with self._option():
                self._token("''")
            self._error("expecting one of: ''")

    @graken
    def _nonquote_character_(self):
        self._letter_()

    @graken
    def _national_character_string_literal_(self):
        self._token('N')

        def sep0():
            with self._group():
                self._separator_()

        def block0():
            self._token("'")
            with self._optional():
                def block1():
                    self._character_representation_()

                self._positive_closure(block1)
            self._token("'")

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _unicode_character_string_literal_(self):
        with self._optional():
            self._token('_')
            self._character_set_name_()
        self._token('U')
        self._token('&')

        def sep0():
            with self._group():
                self._separator_()

        def block0():
            self._token("'")
            with self._optional():
                def block1():
                    self._unicode_representation_()

                self._positive_closure(block1)
            self._token("'")

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token('ESCAPE')
            self._escape_character_()

    @graken
    def _unicode_representation_(self):
        with self._choice():
            with self._option():
                self._character_representation_()
            with self._option():
                self._unicode_escape_value_()
            self._error('no available options')

    @graken
    def _binary_string_literal_(self):
        self._token('X')

        def sep0():
            with self._group():
                self._separator_()

        def block0():
            self._token("'")
            with self._optional():
                def block1():
                    self._hexit_()
                    self._hexit_()

                self._positive_closure(block1)
            self._token("'")

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token('ESCAPE')
            self._escape_character_()

    @graken
    def _hexit_(self):
        self._pattern(r'[a-f\d]')

    @graken
    def _signed_numeric_literal_(self):
        with self._optional():
            self._sign_()
        self._unsigned_numeric_literal_()

    @graken
    def _unsigned_numeric_literal_(self):
        with self._choice():
            with self._option():
                self._exact_numeric_literal_()
            with self._option():
                self._approximate_numeric_literal_()
            self._error('no available options')

    @graken
    def _exact_numeric_literal_(self):
        with self._choice():
            with self._option():
                self._integer_()
                with self._optional():
                    self._token('.')
                    with self._optional():
                        self._integer_()
            with self._option():
                self._token('.')
                self._integer_()
            self._error('no available options')

    @graken
    def _sign_(self):
        with self._choice():
            with self._option():
                self._token('+')
            with self._option():
                self._token('-')
            self._error('expecting one of: + -')

    @graken
    def _approximate_numeric_literal_(self):
        self._exact_numeric_literal_()
        self._token('E')
        self._exponent_()

    @graken
    def _exponent_(self):
        self._signed_integer_()

    @graken
    def _signed_integer_(self):
        with self._optional():
            self._sign_()
        self._integer_()

    @graken
    def _datetime_literal_(self):
        with self._choice():
            with self._option():
                self._date_literal_()
            with self._option():
                self._time_literal_()
            with self._option():
                self._timestamp_literal_()
            self._error('no available options')

    @graken
    def _date_literal_(self):
        self._token('DATE')
        self._date_string_()

    @graken
    def _time_literal_(self):
        self._token('TIME')
        self._time_string_()

    @graken
    def _timestamp_literal_(self):
        self._token('TIMESTAMP')
        self._timestamp_string_()

    @graken
    def _date_string_(self):
        self._token("'")
        self._date_value_()
        self._token("'")

    @graken
    def _time_string_(self):
        self._token("'")
        self._unquoted_time_string_()
        self._token("'")

    @graken
    def _timestamp_string_(self):
        self._token("'")
        self._unquoted_timestamp_string_()
        self._token("'")

    @graken
    def _time_zone_interval_(self):
        self._sign_()
        self._hours_value_()
        self._token(':')
        self._minutes_value_()

    @graken
    def _date_value_(self):
        self._years_value_()
        self._token('-')
        self._months_value_()
        self._token('-')
        self._days_value_()

    @graken
    def _time_value_(self):
        self._hours_value_()
        self._token(':')
        self._minutes_value_()
        self._token(':')
        self._seconds_value_()

    @graken
    def _interval_literal_(self):
        self._token('INTERVAL')
        with self._optional():
            self._sign_()
        self._interval_string_()
        self._interval_qualifier_()

    @graken
    def _interval_string_(self):
        self._token("'")
        self._unquoted_interval_string_()
        self._token("'")

    @graken
    def _unquoted_time_string_(self):
        self._time_value_()
        with self._optional():
            self._time_zone_interval_()

    @graken
    def _unquoted_timestamp_string_(self):
        self._date_value_()
        self._whitespace_()
        self._unquoted_time_string_()

    @graken
    def _unquoted_interval_string_(self):
        with self._optional():
            self._sign_()
        with self._group():
            with self._choice():
                with self._option():
                    self._year_month_literal_()
                with self._option():
                    self._day_time_literal_()
                self._error('no available options')

    @graken
    def _year_month_literal_(self):
        with self._choice():
            with self._option():
                self._years_value_()
            with self._option():
                with self._optional():
                    self._years_value_()
                    self._token('-')
                self._months_value_()
            self._error('no available options')

    @graken
    def _day_time_literal_(self):
        with self._choice():
            with self._option():
                self._day_time_interval_()
            with self._option():
                self._time_interval_()
            self._error('no available options')

    @graken
    def _day_time_interval_(self):
        self._days_value_()
        with self._optional():
            self._whitespace_()
            self._hours_value_()
            with self._optional():
                self._token(':')
                self._minutes_value_()
                with self._optional():
                    self._token(':')
                    self._seconds_value_()

    @graken
    def _time_interval_(self):
        with self._choice():
            with self._option():
                self._hours_value_()
                with self._optional():
                    self._token(':')
                    self._minutes_value_()
                    with self._optional():
                        self._token(':')
                        self._seconds_value_()
            with self._option():
                self._minutes_value_()
                with self._optional():
                    self._token(':')
                    self._seconds_value_()
            with self._option():
                self._seconds_value_()
            self._error('no available options')

    @graken
    def _years_value_(self):
        self._integer_()

    @graken
    def _months_value_(self):
        self._integer_()

    @graken
    def _days_value_(self):
        self._integer_()

    @graken
    def _hours_value_(self):
        self._integer_()

    @graken
    def _minutes_value_(self):
        self._integer_()

    @graken
    def _seconds_value_(self):
        self._integer_()
        with self._optional():
            self._token('.')
            with self._optional():
                self._integer_()

    @graken
    def _boolean_literal_(self):
        with self._choice():
            with self._option():
                self._token('TRUE')
            with self._option():
                self._token('FALSE')
            with self._option():
                self._token('UNKNOWN')
            self._error('expecting one of: FALSE TRUE UNKNOWN')

    @graken
    def _identifier_(self):
        with self._choice():
            with self._option():
                self._regular_identifier_()
            with self._option():
                self._delimited_identifier_()
            self._error('no available options')

    @graken
    def _authorization_identifier_(self):
        with self._choice():
            with self._option():
                self._role_name_()
            with self._option():
                self._user_identifier_()
            self._error('no available options')

    @graken
    def _table_name_(self):
        self._local_or_schema_qualified_name_()

    @graken
    def _domain_name_(self):
        self._schema_qualified_name_()

    @graken
    def _schema_name_(self):
        with self._optional():
            self._catalog_name_()
            self._token('.')
        self._unqualified_schema_name_()

    @graken
    def _unqualified_schema_name_(self):
        self._identifier_()

    @graken
    def _catalog_name_(self):
        self._identifier_()

    @graken
    def _schema_qualified_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _local_or_schema_qualified_name_(self):
        with self._optional():
            self._local_or_schema_qualifier_()
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _local_or_schema_qualifier_(self):
        with self._choice():
            with self._option():
                self._schema_name_()
            with self._option():
                self._token('MODULE')
            self._error('expecting one of: MODULE')

    @graken
    def _qualified_identifier_(self):
        self._identifier_()

    @graken
    def _column_name_(self):
        self._identifier_()

    @graken
    def _correlation_name_(self):
        self._identifier_()

    @graken
    def _query_name_(self):
        self._identifier_()

    @graken
    def _schema_qualified_routine_name_(self):
        self._schema_qualified_name_()

    @graken
    def _method_name_(self):
        self._identifier_()

    @graken
    def _specific_name_(self):
        self._schema_qualified_name_()

    @graken
    def _cursor_name_(self):
        self._local_qualified_name_()

    @graken
    def _local_qualified_name_(self):
        with self._optional():
            self._token('MODULE')
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _host_parameter_name_(self):
        self._token(':')
        self._identifier_()

    @graken
    def _sql_parameter_name_(self):
        self._identifier_()

    @graken
    def _constraint_name_(self):
        self._schema_qualified_name_()

    @graken
    def _external_routine_name_(self):
        with self._choice():
            with self._option():
                self._identifier_()
            with self._option():
                self._character_string_literal_()
            self._error('no available options')

    @graken
    def _trigger_name_(self):
        self._schema_qualified_name_()

    @graken
    def _collation_name_(self):
        self._schema_qualified_name_()

    @graken
    def _character_set_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._regular_identifier_()

    @graken
    def _transliteration_name_(self):
        self._schema_qualified_name_()

    @graken
    def _transcoding_name_(self):
        self._schema_qualified_name_()

    @graken
    def _user_defined_type_name_(self):
        self._schema_qualified_type_name_()

    @graken
    def _schema_resolved_user_defined_type_name_(self):
        self._user_defined_type_name_()

    @graken
    def _schema_qualified_type_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _attribute_name_(self):
        self._identifier_()

    @graken
    def _field_name_(self):
        self._identifier_()

    @graken
    def _savepoint_name_(self):
        self._identifier_()

    @graken
    def _sequence_generator_name_(self):
        self._schema_qualified_name_()

    @graken
    def _role_name_(self):
        self._identifier_()

    @graken
    def _user_identifier_(self):
        self._identifier_()

    @graken
    def _connection_name_(self):
        self._simple_value_specification_()

    @graken
    def _sql_server_name_(self):
        self._simple_value_specification_()

    @graken
    def _connection_user_name_(self):
        self._simple_value_specification_()

    @graken
    def _sql_statement_name_(self):
        with self._choice():
            with self._option():
                self._statement_name_()
            with self._option():
                self._extended_statement_name_()
            self._error('no available options')

    @graken
    def _statement_name_(self):
        self._identifier_()

    @graken
    def _extended_statement_name_(self):
        with self._optional():
            self._scope_option_()
        self._simple_value_specification_()

    @graken
    def _dynamic_cursor_name_(self):
        with self._choice():
            with self._option():
                self._cursor_name_()
            with self._option():
                self._extended_cursor_name_()
            self._error('no available options')

    @graken
    def _extended_cursor_name_(self):
        with self._optional():
            self._scope_option_()
        self._simple_value_specification_()

    @graken
    def _descriptor_name_(self):
        with self._optional():
            self._scope_option_()
        self._simple_value_specification_()

    @graken
    def _scope_option_(self):
        with self._choice():
            with self._option():
                self._token('GLOBAL')
            with self._option():
                self._token('LOCAL')
            self._error('expecting one of: GLOBAL LOCAL')

    @graken
    def _window_name_(self):
        self._identifier_()

    @graken
    def _data_type_(self):
        with self._choice():
            with self._option():
                self._predefined_type_()
            with self._option():
                self._row_type_()
            with self._option():
                self._path_resolved_user_defined_type_name_()
            with self._option():
                self._reference_type_()
            with self._option():
                self._collection_type_()
            self._error('no available options')

    @graken
    def _predefined_type_(self):
        with self._choice():
            with self._option():
                self._character_string_type_()
                with self._optional():
                    self._token('CHARACTER')
                    self._token('SET')
                    self._character_set_name_()
                with self._optional():
                    self._collate_clause_()
            with self._option():
                self._national_character_string_type_()
                with self._optional():
                    self._collate_clause_()
            with self._option():
                self._binary_large_object_string_type_()
            with self._option():
                self._numeric_type_()
            with self._option():
                self._token('BOOLEAN')
            with self._option():
                self._datetime_type_()
            with self._option():
                self._interval_type_()
            self._error('expecting one of: BOOLEAN')

    @graken
    def _character_string_type_(self):
        with self._choice():
            with self._option():
                self._token('CHARACTER')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('CHAR')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('CHARACTER')
                self._token('VARYING')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('CHAR')
                self._token('VARYING')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('VARCHAR')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('CHARACTER')
                self._token('LARGE')
                self._token('OBJECT')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            with self._option():
                self._token('CHAR')
                self._token('LARGE')
                self._token('OBJECT')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            with self._option():
                self._token('CLOB')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            self._error('expecting one of: CHAR CHARACTER CLOB')

    @graken
    def _national_character_string_type_(self):
        with self._choice():
            with self._option():
                self._token('NATIONAL')
                self._token('CHARACTER')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('NATIONAL')
                self._token('CHAR')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('NCHAR')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('NATIONAL')
                self._token('CHARACTER')
                self._token('VARYING')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('NATIONAL')
                self._token('CHAR')
                self._token('VARYING')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('NCHAR')
                self._token('VARYING')
                self._token('(')
                self._integer_()
                self._token(')')
            with self._option():
                self._token('NATIONAL')
                self._token('CHARACTER')
                self._token('LARGE')
                self._token('OBJECT')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            with self._option():
                self._token('NCHAR')
                self._token('LARGE')
                self._token('OBJECT')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            with self._option():
                self._token('NCLOB')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            self._error('expecting one of: NATIONAL NCHAR NCLOB')

    @graken
    def _binary_large_object_string_type_(self):
        with self._choice():
            with self._option():
                self._token('BINARY')
                self._token('LARGE')
                self._token('OBJECT')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            with self._option():
                self._token('BLOB')
                with self._optional():
                    self._token('(')
                    self._large_object_length_()
                    self._token(')')
            self._error('expecting one of: BINARY BLOB')

    @graken
    def _numeric_type_(self):
        with self._choice():
            with self._option():
                self._exact_numeric_type_()
            with self._option():
                self._approximate_numeric_type_()
            self._error('no available options')

    @graken
    def _exact_numeric_type_(self):
        with self._choice():
            with self._option():
                self._token('NUMERIC')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    with self._optional():
                        self._token(',')
                        self._integer_()
                    self._token(')')
            with self._option():
                self._token('DECIMAL')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    with self._optional():
                        self._token(',')
                        self._integer_()
                    self._token(')')
            with self._option():
                self._token('DEC')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    with self._optional():
                        self._token(',')
                        self._integer_()
                    self._token(')')
            with self._option():
                self._token('SMALLINT')
            with self._option():
                self._token('INTEGER')
            with self._option():
                self._token('INT')
            with self._option():
                self._token('BIGINT')
            self._error('expecting one of: BIGINT DEC DECIMAL INT INTEGER '
                        'NUMERIC SMALLINT')

    @graken
    def _approximate_numeric_type_(self):
        with self._choice():
            with self._option():
                self._token('FLOAT')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('REAL')
            with self._option():
                self._token('DOUBLE')
                self._token('integer')
            self._error('expecting one of: DOUBLE FLOAT REAL')

    @graken
    def _large_object_length_(self):
        with self._choice():
            with self._option():
                self._integer_()
                with self._optional():
                    self._multiplier_()
                with self._optional():
                    self._char_length_units_()
            with self._option():
                self._large_object_length_token_()
                with self._optional():
                    self._char_length_units_()
            self._error('no available options')

    @graken
    def _char_length_units_(self):
        with self._choice():
            with self._option():
                self._token('CHARACTERS')
            with self._option():
                self._token('CODE_UNITS')
            with self._option():
                self._token('OCTETS')
            self._error('expecting one of: CHARACTERS CODE_UNITS OCTETS')

    @graken
    def _datetime_type_(self):
        with self._choice():
            with self._option():
                self._token('DATE')
            with self._option():
                self._token('TIME')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
                with self._optional():
                    self._with_or_without_time_zone_()
            with self._option():
                self._token('TIMESTAMP')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
                with self._optional():
                    self._with_or_without_time_zone_()
            self._error('expecting one of: DATE TIME TIMESTAMP')

    @graken
    def _with_or_without_time_zone_(self):
        with self._choice():
            with self._option():
                self._token('WITH')
                self._token('TIME')
                self._token('ZONE')
            with self._option():
                self._token('WITHOUT')
                self._token('TIME')
                self._token('ZONE')
            self._error('expecting one of: WITH WITHOUT')

    @graken
    def _interval_type_(self):
        self._token('INTERVAL')
        self._interval_qualifier_()

    @graken
    def _row_type_(self):
        self._token('ROW')
        self._row_type_body_()

    @graken
    def _row_type_body_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._field_definition_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _reference_type_(self):
        self._token('REF')
        self._token('(')
        self._referenced_type_()
        self._token(')')
        with self._optional():
            self._scope_clause_()

    @graken
    def _scope_clause_(self):
        self._token('SCOPE')
        self._table_name_()

    @graken
    def _referenced_type_(self):
        self._path_resolved_user_defined_type_name_()

    @graken
    def _path_resolved_user_defined_type_name_(self):
        self._user_defined_type_name_()

    @graken
    def _collection_type_(self):
        with self._choice():
            with self._option():
                self._array_type_()
            with self._option():
                self._multiset_type_()
            self._error('no available options')

    @graken
    def _array_type_(self):
        self._data_type_()
        self._token('ARRAY')
        with self._optional():
            self._left_bracket_or_trigraph_()
            self._integer_()
            self._right_bracket_or_trigraph_()

    @graken
    def _multiset_type_(self):
        self._data_type_()
        self._token('MULTISET')

    @graken
    def _field_definition_(self):
        self._field_name_()
        self._data_type_()
        with self._optional():
            self._reference_scope_check_()

    @graken
    def _value_expression_primary_(self):
        with self._choice():
            with self._option():
                self._parenthesized_value_expression_()
            with self._option():
                self._nonparenthesized_value_expression_primary_()
            self._error('no available options')

    @graken
    def _parenthesized_value_expression_(self):
        self._token('(')
        self._value_expression_()
        self._token(')')

    @graken
    def _nonparenthesized_value_expression_primary_(self):
        with self._choice():
            with self._option():
                self._unsigned_value_specification_()
            with self._option():
                self._column_reference_()
            with self._option():
                self._set_function_specification_()
            with self._option():
                self._window_function_()
            with self._option():
                self._subquery_()
            with self._option():
                self._case_expression_()
            with self._option():
                self._cast_specification_()
            with self._option():
                self._field_reference_()
            with self._option():
                self._subtype_treatment_()
            with self._option():
                self._method_invocation_()
            with self._option():
                self._static_method_invocation_()
            with self._option():
                self._token('NEW')
                self._routine_invocation_()
            with self._option():
                self._attribute_or_method_reference_()
            with self._option():
                self._reference_resolution_()
            with self._option():
                self._collection_value_constructor_()
            with self._option():
                self._array_element_reference_()
            with self._option():
                self._multiset_element_reference_()
            with self._option():
                self._routine_invocation_()
            with self._option():
                self._next_value_expression_()
            self._error('no available options')

    @graken
    def _value_specification_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._general_value_specification_()
            self._error('no available options')

    @graken
    def _unsigned_value_specification_(self):
        with self._choice():
            with self._option():
                self._unsigned_literal_()
            with self._option():
                self._general_value_specification_()
            self._error('no available options')

    @graken
    def _general_value_specification_(self):
        with self._choice():
            with self._option():
                self._host_parameter_specification_()
            with self._option():
                self._sql_parameter_reference_()
            with self._option():
                self._token('?')
            with self._option():
                self._current_collation_specification_()
            with self._option():
                self._token('CURRENT_DEFAULT_TRANSFORM_GROUP')
            with self._option():
                self._token('CURRENT_PATH')
            with self._option():
                self._token('CURRENT_ROLE')
            with self._option():
                self._token('CURRENT_TRANSFORM_GROUP_FOR_TYPE')
                self._path_resolved_user_defined_type_name_()
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
            self._error('expecting one of: CURRENT_DEFAULT_TRANSFORM_GROUP '
                        'CURRENT_PATH CURRENT_ROLE CURRENT_USER SESSION_USER '
                        'SYSTEM_USER USER VALUE')

    @graken
    def _simple_value_specification_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._host_parameter_name_()
            with self._option():
                self._sql_parameter_reference_()
            self._error('no available options')

    @graken
    def _target_specification_(self):
        with self._choice():
            with self._option():
                self._host_parameter_specification_()
            with self._option():
                self._sql_parameter_reference_()
            with self._option():
                self._column_reference_()
            with self._option():
                self._target_array_element_specification_()
            with self._option():
                self._token('?')
            self._error('expecting one of: ?')

    @graken
    def _simple_target_specification_(self):
        with self._choice():
            with self._option():
                self._host_parameter_specification_()
            with self._option():
                self._sql_parameter_reference_()
            with self._option():
                self._column_reference_()
            self._error('no available options')

    @graken
    def _host_parameter_specification_(self):
        self._host_parameter_name_()
        with self._optional():
            self._indicator_parameter_()

    @graken
    def _indicator_parameter_(self):
        with self._optional():
            self._token('INDICATOR')
        self._host_parameter_name_()

    @graken
    def _target_array_element_specification_(self):
        self._target_array_reference_()
        self._left_bracket_or_trigraph_()
        self._simple_value_specification_()
        self._right_bracket_or_trigraph_()

    @graken
    def _target_array_reference_(self):
        with self._choice():
            with self._option():
                self._sql_parameter_reference_()
            with self._option():
                self._column_reference_()
            self._error('no available options')

    @graken
    def _current_collation_specification_(self):
        self._token('CURRENT_COLLATION')
        self._token('(')
        self._string_value_expression_()
        self._token(')')

    @graken
    def _contextually_typed_value_specification_(self):
        with self._choice():
            with self._option():
                self._implicitly_typed_value_specification_()
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT')

    @graken
    def _implicitly_typed_value_specification_(self):
        with self._choice():
            with self._option():
                self._token('NULL')
            with self._option():
                self._empty_specification_()
            self._error('expecting one of: NULL')

    @graken
    def _empty_specification_(self):
        with self._choice():
            with self._option():
                self._token('ARRAY')
                self._left_bracket_or_trigraph_()
                self._right_bracket_or_trigraph_()
            with self._option():
                self._token('MULTISET')
                self._left_bracket_or_trigraph_()
                self._right_bracket_or_trigraph_()
            self._error('no available options')

    @graken
    def _identifier_chain_(self):
        def sep0():
            self._token('.')

        def block0():
            self._identifier_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _basic_identifier_chain_(self):
        self._identifier_chain_()

    @graken
    def _column_reference_(self):
        with self._choice():
            with self._option():
                self._basic_identifier_chain_()
            with self._option():
                self._token('MODULE')
                self._token('.')
                self._qualified_identifier_()
                self._token('.')
                self._column_name_()
            self._error('no available options')

    @graken
    def _sql_parameter_reference_(self):
        self._basic_identifier_chain_()

    @graken
    def _set_function_specification_(self):
        with self._choice():
            with self._option():
                self._aggregate_function_()
            with self._option():
                self._grouping_operation_()
            self._error('no available options')

    @graken
    def _grouping_operation_(self):
        self._token('GROUPING')
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._column_reference_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _window_function_(self):
        self._window_function_type_()
        self._token('OVER')
        self._window_name_or_specification_()

    @graken
    def _window_function_type_(self):
        with self._choice():
            with self._option():
                self._rank_function_type_()
                self._empty_grouping_set_()
            with self._option():
                self._token('ROW_NUMBER')
                self._empty_grouping_set_()
            with self._option():
                self._aggregate_function_()
            self._error('no available options')

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
            self._error('expecting one of: CUME_DIST DENSE_RANK PERCENT_RANK '
                        'RANK')

    @graken
    def _window_name_or_specification_(self):
        with self._choice():
            with self._option():
                self._window_name_()
            with self._option():
                self._window_specification_()
            self._error('no available options')

    @graken
    def _case_expression_(self):
        with self._choice():
            with self._option():
                self._case_abbreviation_()
            with self._option():
                self._case_specification_()
            self._error('no available options')

    @graken
    def _case_abbreviation_(self):
        with self._choice():
            with self._option():
                self._token('NULLIF')
                self._token('(')
                self._value_expression_()
                self._token(',')
                self._value_expression_()
                self._token(')')
            with self._option():
                self._token('COALESCE')
                self._token('(')
                self._value_expression_()

                def block0():
                    self._token(',')
                    self._value_expression_()

                self._positive_closure(block0)
                self._token(')')
            self._error('no available options')

    @graken
    def _case_specification_(self):
        with self._choice():
            with self._option():
                self._simple_case_()
            with self._option():
                self._searched_case_()
            self._error('no available options')

    @graken
    def _simple_case_(self):
        self._token('CASE')
        self._case_operand_()

        def block0():
            self._simple_when_clause_()

        self._positive_closure(block0)
        with self._optional():
            self._else_clause_()
        self._token('END')

    @graken
    def _searched_case_(self):
        self._token('CASE')

        def block0():
            self._searched_when_clause_()

        self._positive_closure(block0)
        with self._optional():
            self._else_clause_()
        self._token('END')

    @graken
    def _simple_when_clause_(self):
        self._token('WHEN')
        self._when_operand_()
        self._token('THEN')
        self._result_()

    @graken
    def _searched_when_clause_(self):
        self._token('WHEN')
        self._search_condition_()
        self._token('THEN')
        self._result_()

    @graken
    def _else_clause_(self):
        self._token('ELSE')
        self._result_()

    @graken
    def _case_operand_(self):
        with self._choice():
            with self._option():
                self._row_value_predicand_()
            with self._option():
                self._overlaps_predicate_()
            self._error('no available options')

    @graken
    def _when_operand_(self):
        with self._choice():
            with self._option():
                self._row_value_predicand_()
            with self._option():
                self._comp_op_()
                self._row_value_predicand_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('BETWEEN')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ASYMMETRIC')
                        with self._option():
                            self._token('SYMMETRIC')
                        self._error('expecting one of: ASYMMETRIC SYMMETRIC')
                self._row_value_predicand_()
                self._token('AND')
                self._row_value_predicand_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('IN')
                self._in_predicate_value_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('LIKE')
                self._character_pattern_()
                with self._optional():
                    self._token('ESCAPE')
                    self._escape_character_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('LIKE')
                self._octet_pattern_()
                with self._optional():
                    self._token('ESCAPE')
                    self._escape_octet_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('SIMILAR')
                self._token('TO')
                self._similar_pattern_()
                with self._optional():
                    self._token('ESCAPE')
                    self._escape_character_()
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('NULL')
            with self._option():
                self._comp_op_()
                self._quantifier_()
                self._subquery_()
            with self._option():
                self._token('MATCH')
                with self._optional():
                    self._token('UNIQUE')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('SIMPLE')
                        with self._option():
                            self._token('PARTIAL')
                        with self._option():
                            self._token('FULL')
                        self._error('expecting one of: FULL PARTIAL SIMPLE')
                self._subquery_()
            with self._option():
                self._token('OVERLAPS')
                self._row_value_predicand_()
            with self._option():
                self._token('IS')
                self._token('DISTINCT')
                self._token('FROM')
                self._row_value_predicand_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('MEMBER')
                with self._optional():
                    self._token('OF')
                self._multiset_value_expression_()
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('SUBMULTISET')
                with self._optional():
                    self._token('OF')
                self._multiset_value_expression_()
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('A')
                self._token('SET')
            with self._option():
                self._token('IS')
                with self._optional():
                    self._token('NOT')
                self._token('OF')
                self._token('(')
                self._type_list_()
                self._token(')')
            self._error('expecting one of: IS')

    @graken
    def _result_(self):
        with self._choice():
            with self._option():
                self._result_expression_()
            with self._option():
                self._token('NULL')
            self._error('expecting one of: NULL')

    @graken
    def _result_expression_(self):
        self._value_expression_()

    @graken
    def _cast_specification_(self):
        self._token('CAST')
        self._token('(')
        self._cast_operand_()
        self._token('AS')
        self._cast_target_()
        self._token(')')

    @graken
    def _cast_operand_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._implicitly_typed_value_specification_()
            self._error('no available options')

    @graken
    def _cast_target_(self):
        with self._choice():
            with self._option():
                self._domain_name_()
            with self._option():
                self._data_type_()
            self._error('no available options')

    @graken
    def _next_value_expression_(self):
        self._token('NEXT')
        self._token('VALUE')
        self._token('FOR')
        self._sequence_generator_name_()

    @graken
    def _field_reference_(self):
        self._value_expression_primary_()
        self._token('.')
        self._field_name_()

    @graken
    def _subtype_treatment_(self):
        self._token('TREAT')
        self._token('(')
        self._subtype_operand_()
        self._token('AS')
        self._target_subtype_()
        self._token(')')

    @graken
    def _subtype_operand_(self):
        self._value_expression_()

    @graken
    def _target_subtype_(self):
        with self._choice():
            with self._option():
                self._path_resolved_user_defined_type_name_()
            with self._option():
                self._reference_type_()
            self._error('no available options')

    @graken
    def _method_invocation_(self):
        with self._choice():
            with self._option():
                self._direct_invocation_()
            with self._option():
                self._generalized_invocation_()
            self._error('no available options')

    @graken
    def _direct_invocation_(self):
        self._value_expression_primary_()
        self._token('.')
        self._method_name_()
        with self._optional():
            self._sql_argument_list_()

    @graken
    def _generalized_invocation_(self):
        self._token('(')
        self._value_expression_primary_()
        self._token('AS')
        self._data_type_()
        self._token(')')
        self._token('.')
        self._method_name_()
        with self._optional():
            self._sql_argument_list_()

    @graken
    def _static_method_invocation_(self):
        self._path_resolved_user_defined_type_name_()
        self._token('::')
        self._method_name_()
        with self._optional():
            self._sql_argument_list_()

    @graken
    def _attribute_or_method_reference_(self):
        self._value_expression_primary_()
        self._dereference_operator_()
        self._qualified_identifier_()
        with self._optional():
            self._sql_argument_list_()

    @graken
    def _dereference_operator_(self):
        self._token('->')

    @graken
    def _reference_resolution_(self):
        self._token('DEREF')
        self._token('(')
        self._reference_value_expression_()
        self._token(')')

    @graken
    def _array_element_reference_(self):
        self._array_value_expression_()
        self._left_bracket_or_trigraph_()
        self._numeric_value_expression_()
        self._right_bracket_or_trigraph_()

    @graken
    def _multiset_element_reference_(self):
        self._token('ELEMENT')
        self._token('(')
        self._multiset_value_expression_()
        self._token(')')

    @graken
    def _value_expression_(self):
        with self._choice():
            with self._option():
                self._common_value_expression_()
            with self._option():
                self._boolean_value_expression_()
            with self._option():
                self._row_value_expression_()
            self._error('no available options')

    @graken
    def _common_value_expression_(self):
        with self._choice():
            with self._option():
                self._numeric_value_expression_()
            with self._option():
                self._string_value_expression_()
            with self._option():
                self._datetime_value_expression_()
            with self._option():
                self._interval_value_expression_()
            with self._option():
                self._user_defined_type_value_expression_()
            with self._option():
                self._reference_value_expression_()
            with self._option():
                self._collection_value_expression_()
            self._error('no available options')

    @graken
    def _user_defined_type_value_expression_(self):
        self._value_expression_primary_()

    @graken
    def _reference_value_expression_(self):
        self._value_expression_primary_()

    @graken
    def _collection_value_expression_(self):
        with self._choice():
            with self._option():
                self._array_value_expression_()
            with self._option():
                self._multiset_value_expression_()
            self._error('no available options')

    @graken
    def _collection_value_constructor_(self):
        with self._choice():
            with self._option():
                self._array_value_constructor_()
            with self._option():
                self._multiset_value_constructor_()
            self._error('no available options')

    @graken
    def _numeric_value_expression_(self):
        with self._choice():
            with self._option():
                self._term_()
            with self._option():
                self._numeric_value_expression_()
                self._token('+')
                self._term_()
            with self._option():
                self._numeric_value_expression_()
                self._token('-')
                self._term_()
            self._error('no available options')

    @graken
    def _term_(self):
        with self._choice():
            with self._option():
                self._factor_()
            with self._option():
                self._term_()
                self._token('*')
                self._factor_()
            with self._option():
                self._term_()
                self._token('/')
                self._factor_()
            self._error('no available options')

    @graken
    def _factor_(self):
        with self._optional():
            self._sign_()
        self._numeric_primary_()

    @graken
    def _numeric_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
            with self._option():
                self._numeric_value_function_()
            self._error('no available options')

    @graken
    def _numeric_value_function_(self):
        with self._choice():
            with self._option():
                self._position_expression_()
            with self._option():
                self._extract_expression_()
            with self._option():
                self._length_expression_()
            with self._option():
                self._cardinality_expression_()
            with self._option():
                self._absolute_value_expression_()
            with self._option():
                self._modulus_expression_()
            with self._option():
                self._natural_logarithm_()
            with self._option():
                self._exponential_function_()
            with self._option():
                self._power_function_()
            with self._option():
                self._square_root_()
            with self._option():
                self._floor_function_()
            with self._option():
                self._ceiling_function_()
            with self._option():
                self._width_bucket_function_()
            self._error('no available options')

    @graken
    def _position_expression_(self):
        with self._choice():
            with self._option():
                self._string_position_expression_()
            with self._option():
                self._blob_position_expression_()
            self._error('no available options')

    @graken
    def _string_position_expression_(self):
        self._token('POSITION')
        self._token('(')
        self._string_value_expression_()
        self._token('IN')
        self._string_value_expression_()
        with self._optional():
            self._token('USING')
            self._char_length_units_()
        self._token(')')

    @graken
    def _blob_position_expression_(self):
        self._token('POSITION')
        self._token('(')
        self._blob_value_expression_()
        self._token('IN')
        self._blob_value_expression_()
        self._token(')')

    @graken
    def _length_expression_(self):
        with self._choice():
            with self._option():
                self._char_length_expression_()
            with self._option():
                self._octet_length_expression_()
            self._error('no available options')

    @graken
    def _char_length_expression_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('CHAR_LENGTH')
                with self._option():
                    self._token('CHARACTER_LENGTH')
                self._error('expecting one of: CHARACTER_LENGTH CHAR_LENGTH')
        self._token('(')
        self._string_value_expression_()
        with self._optional():
            self._token('USING')
            self._char_length_units_()
        self._token(')')

    @graken
    def _octet_length_expression_(self):
        self._token('OCTET_LENGTH')
        self._token('(')
        self._string_value_expression_()
        self._token(')')

    @graken
    def _extract_expression_(self):
        self._token('EXTRACT')
        self._token('(')
        self._extract_field_()
        self._token('FROM')
        self._extract_source_()
        self._token(')')

    @graken
    def _extract_field_(self):
        with self._choice():
            with self._option():
                self._primary_datetime_field_()
            with self._option():
                self._time_zone_field_()
            self._error('no available options')

    @graken
    def _time_zone_field_(self):
        with self._choice():
            with self._option():
                self._token('TIMEZONE_HOUR')
            with self._option():
                self._token('TIMEZONE_MINUTE')
            self._error('expecting one of: TIMEZONE_HOUR TIMEZONE_MINUTE')

    @graken
    def _extract_source_(self):
        with self._choice():
            with self._option():
                self._datetime_value_expression_()
            with self._option():
                self._interval_value_expression_()
            self._error('no available options')

    @graken
    def _cardinality_expression_(self):
        self._token('CARDINALITY')
        self._token('(')
        self._collection_value_expression_()
        self._token(')')

    @graken
    def _absolute_value_expression_(self):
        self._token('ABS')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _modulus_expression_(self):
        self._token('MOD')
        self._token('(')
        self._numeric_value_expression_()
        self._token(',')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _natural_logarithm_(self):
        self._token('LN')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _exponential_function_(self):
        self._token('EXP')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _power_function_(self):
        self._token('POWER')
        self._token('(')
        self._numeric_value_expression_()
        self._token(',')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _square_root_(self):
        self._token('SQRT')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _floor_function_(self):
        self._token('FLOOR')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _ceiling_function_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('CEIL')
                with self._option():
                    self._token('CEILING')
                self._error('expecting one of: CEIL CEILING')
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')

    @graken
    def _width_bucket_function_(self):
        self._token('WIDTH_BUCKET')
        self._token('(')
        self._width_bucket_operand_()
        self._token(',')
        self._numeric_value_expression_()
        self._token(',')
        self._numeric_value_expression_()
        self._token(',')
        self._width_bucket_count_()
        self._token(')')

    @graken
    def _width_bucket_operand_(self):
        self._numeric_value_expression_()

    @graken
    def _width_bucket_count_(self):
        self._numeric_value_expression_()

    @graken
    def _string_value_expression_(self):
        with self._choice():
            with self._option():
                self._character_value_expression_()
            with self._option():
                self._blob_value_expression_()
            self._error('no available options')

    @graken
    def _character_value_expression_(self):
        with self._choice():
            with self._option():
                self._concatenation_()
            with self._option():
                self._character_factor_()
            self._error('no available options')

    @graken
    def _concatenation_(self):
        self._character_value_expression_()
        self._token('||')
        self._character_factor_()

    @graken
    def _character_factor_(self):
        self._character_primary_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _character_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
            with self._option():
                self._string_value_function_()
            self._error('no available options')

    @graken
    def _blob_value_expression_(self):
        with self._choice():
            with self._option():
                self._blob_concatenation_()
            with self._option():
                self._blob_primary_()
            self._error('no available options')

    @graken
    def _blob_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
            with self._option():
                self._string_value_function_()
            self._error('no available options')

    @graken
    def _blob_concatenation_(self):
        self._blob_value_expression_()
        self._token('||')
        self._blob_primary_()

    @graken
    def _string_value_function_(self):
        with self._choice():
            with self._option():
                self._character_value_function_()
            with self._option():
                self._blob_value_function_()
            self._error('no available options')

    @graken
    def _character_value_function_(self):
        with self._choice():
            with self._option():
                self._character_substring_function_()
            with self._option():
                self._regular_expression_substring_function_()
            with self._option():
                self._fold_()
            with self._option():
                self._transcoding_()
            with self._option():
                self._character_transliteration_()
            with self._option():
                self._trim_function_()
            with self._option():
                self._character_overlay_function_()
            with self._option():
                self._normalize_function_()
            with self._option():
                self._specific_type_method_()
            self._error('no available options')

    @graken
    def _character_substring_function_(self):
        self._token('SUBSTRING')
        self._token('(')
        self._character_value_expression_()
        self._token('FROM')
        self._start_position_()
        with self._optional():
            self._token('FOR')
            self._string_length_()
        with self._optional():
            self._token('USING')
            self._char_length_units_()
        self._token(')')

    @graken
    def _regular_expression_substring_function_(self):
        self._token('SUBSTRING')
        self._token('(')
        self._character_value_expression_()
        self._token('SIMILAR')
        self._character_value_expression_()
        self._token('ESCAPE')
        self._escape_character_()
        self._token(')')

    @graken
    def _fold_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('UPPER')
                with self._option():
                    self._token('LOWER')
                self._error('expecting one of: LOWER UPPER')
        self._token('(')
        self._character_value_expression_()
        self._token(')')

    @graken
    def _transcoding_(self):
        self._token('CONVERT')
        self._token('(')
        self._character_value_expression_()
        self._token('USING')
        self._transcoding_name_()
        self._token(')')

    @graken
    def _character_transliteration_(self):
        self._token('TRANSLATE')
        self._token('(')
        self._character_value_expression_()
        self._token('USING')
        self._transliteration_name_()
        self._token(')')

    @graken
    def _trim_function_(self):
        self._token('TRIM')
        self._token('(')
        self._trim_operands_()
        self._token(')')

    @graken
    def _trim_operands_(self):
        with self._optional():
            with self._optional():
                self._trim_specification_()
            with self._optional():
                self._trim_character_()
            self._token('FROM')
        self._trim_source_()

    @graken
    def _trim_source_(self):
        self._character_value_expression_()

    @graken
    def _trim_specification_(self):
        with self._choice():
            with self._option():
                self._token('LEADING')
            with self._option():
                self._token('TRAILING')
            with self._option():
                self._token('BOTH')
            self._error('expecting one of: BOTH LEADING TRAILING')

    @graken
    def _trim_character_(self):
        self._character_value_expression_()

    @graken
    def _character_overlay_function_(self):
        self._token('OVERLAY')
        self._token('(')
        self._character_value_expression_()
        self._token('PLACING')
        self._character_value_expression_()
        self._token('FROM')
        self._start_position_()
        with self._optional():
            self._token('FOR')
            self._string_length_()
        with self._optional():
            self._token('USING')
            self._char_length_units_()
        self._token(')')

    @graken
    def _normalize_function_(self):
        self._token('NORMALIZE')
        self._token('(')
        self._character_value_expression_()
        self._token(')')

    @graken
    def _specific_type_method_(self):
        self._user_defined_type_value_expression_()
        self._token('.')
        self._token('SPECIFICTYPE')

    @graken
    def _blob_value_function_(self):
        with self._choice():
            with self._option():
                self._blob_substring_function_()
            with self._option():
                self._blob_trim_function_()
            with self._option():
                self._blob_overlay_function_()
            self._error('no available options')

    @graken
    def _blob_substring_function_(self):
        self._token('SUBSTRING')
        self._token('(')
        self._blob_value_expression_()
        self._token('FROM')
        self._start_position_()
        with self._optional():
            self._token('FOR')
            self._string_length_()
        self._token(')')

    @graken
    def _blob_trim_function_(self):
        self._token('TRIM')
        self._token('(')
        self._blob_trim_operands_()
        self._token(')')

    @graken
    def _blob_trim_operands_(self):
        with self._optional():
            with self._optional():
                self._trim_specification_()
            with self._optional():
                self._blob_value_expression_()
            self._token('FROM')
        self._blob_value_expression_()

    @graken
    def _blob_overlay_function_(self):
        self._token('OVERLAY')
        self._token('(')
        self._blob_value_expression_()
        self._token('PLACING')
        self._blob_value_expression_()
        self._token('FROM')
        self._start_position_()
        with self._optional():
            self._token('FOR')
            self._string_length_()
        self._token(')')

    @graken
    def _start_position_(self):
        self._numeric_value_expression_()

    @graken
    def _string_length_(self):
        self._numeric_value_expression_()

    @graken
    def _datetime_value_expression_(self):
        with self._choice():
            with self._option():
                self._datetime_term_()
            with self._option():
                self._interval_value_expression_()
                self._token('+')
                self._datetime_term_()
            with self._option():
                self._datetime_value_expression_()
                self._token('+')
                self._interval_term_()
            with self._option():
                self._datetime_value_expression_()
                self._token('-')
                self._interval_term_()
            self._error('no available options')

    @graken
    def _datetime_term_(self):
        self._datetime_factor_()

    @graken
    def _datetime_factor_(self):
        self._datetime_primary_()
        with self._optional():
            self._time_zone_()

    @graken
    def _datetime_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
            with self._option():
                self._datetime_value_function_()
            self._error('no available options')

    @graken
    def _time_zone_(self):
        self._token('AT')
        self._time_zone_specifier_()

    @graken
    def _time_zone_specifier_(self):
        with self._choice():
            with self._option():
                self._token('LOCAL')
            with self._option():
                self._token('TIME')
                self._token('ZONE')
                self._interval_primary_()
            self._error('expecting one of: LOCAL')

    @graken
    def _datetime_value_function_(self):
        with self._choice():
            with self._option():
                self._current_date_value_function_()
            with self._option():
                self._current_time_value_function_()
            with self._option():
                self._current_timestamp_value_function_()
            with self._option():
                self._current_local_time_value_function_()
            with self._option():
                self._current_local_timestamp_value_function_()
            self._error('no available options')

    @graken
    def _current_date_value_function_(self):
        self._token('CURRENT_DATE')

    @graken
    def _current_time_value_function_(self):
        self._token('CURRENT_TIME')
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _current_local_time_value_function_(self):
        self._token('LOCALTIME')
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _current_timestamp_value_function_(self):
        self._token('CURRENT_TIMESTAMP')
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _current_local_timestamp_value_function_(self):
        self._token('LOCALTIMESTAMP')
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _interval_value_expression_(self):
        with self._choice():
            with self._option():
                self._interval_term_()
            with self._option():
                self._interval_value_expression_()
                self._token('+')
                self._interval_term_()
            with self._option():
                self._interval_value_expression_()
                self._token('-')
                self._interval_term_()
            with self._option():
                self._token('(')
                self._datetime_value_expression_()
                self._token('-')
                self._datetime_term_()
                self._token(')')
                self._interval_qualifier_()
            self._error('no available options')

    @graken
    def _interval_term_(self):
        with self._choice():
            with self._option():
                self._interval_factor_()
            with self._option():
                self._interval_term_()
                self._token('*')
                self._factor_()
            with self._option():
                self._interval_term_()
                self._token('/')
                self._factor_()
            with self._option():
                self._term_()
                self._token('*')
                self._interval_factor_()
            self._error('no available options')

    @graken
    def _interval_factor_(self):
        with self._optional():
            self._sign_()
        self._interval_primary_()

    @graken
    def _interval_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
                with self._optional():
                    self._interval_qualifier_()
            with self._option():
                self._interval_value_function_()
            self._error('no available options')

    @graken
    def _interval_value_function_(self):
        self._interval_absolute_value_function_()

    @graken
    def _interval_absolute_value_function_(self):
        self._token('ABS')
        self._token('(')
        self._interval_value_expression_()
        self._token(')')

    @graken
    def _boolean_value_expression_(self):
        with self._choice():
            with self._option():
                self._boolean_term_()
            with self._option():
                self._boolean_value_expression_()
                self._token('OR')
                self._boolean_term_()
            self._error('no available options')

    @graken
    def _boolean_term_(self):
        with self._choice():
            with self._option():
                self._boolean_factor_()
            with self._option():
                self._boolean_term_()
                self._token('AND')
                self._boolean_factor_()
            self._error('no available options')

    @graken
    def _boolean_factor_(self):
        with self._optional():
            self._token('NOT')
        self._boolean_test_()

    @graken
    def _boolean_test_(self):
        self._boolean_primary_()
        with self._optional():
            self._token('IS')
            with self._optional():
                self._token('NOT')
            self._truth_value_()

    @graken
    def _truth_value_(self):
        with self._choice():
            with self._option():
                self._token('TRUE')
            with self._option():
                self._token('FALSE')
            with self._option():
                self._token('UNKNOWN')
            self._error('expecting one of: FALSE TRUE UNKNOWN')

    @graken
    def _boolean_primary_(self):
        with self._choice():
            with self._option():
                self._predicate_()
            with self._option():
                self._boolean_predicand_()
            self._error('no available options')

    @graken
    def _boolean_predicand_(self):
        with self._choice():
            with self._option():
                self._parenthesized_boolean_value_expression_()
            with self._option():
                self._nonparenthesized_value_expression_primary_()
            self._error('no available options')

    @graken
    def _parenthesized_boolean_value_expression_(self):
        self._token('(')
        self._boolean_value_expression_()
        self._token(')')

    @graken
    def _array_value_expression_(self):
        with self._choice():
            with self._option():
                self._array_concatenation_()
            with self._option():
                self._array_factor_()
            self._error('no available options')

    @graken
    def _array_concatenation_(self):
        self._array_value_expression_()
        self._token('||')
        self._array_factor_()

    @graken
    def _array_factor_(self):
        self._value_expression_primary_()

    @graken
    def _array_value_constructor_(self):
        with self._choice():
            with self._option():
                self._array_value_constructor_by_enumeration_()
            with self._option():
                self._array_value_constructor_by_query_()
            self._error('no available options')

    @graken
    def _array_value_constructor_by_enumeration_(self):
        self._token('ARRAY')
        self._left_bracket_or_trigraph_()
        self._array_element_list_()
        self._right_bracket_or_trigraph_()

    @graken
    def _array_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._array_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _array_element_(self):
        self._value_expression_()

    @graken
    def _array_value_constructor_by_query_(self):
        self._token('ARRAY')
        self._token('(')
        self._query_expression_()
        with self._optional():
            self._order_by_clause_()
        self._token(')')

    @graken
    def _multiset_value_expression_(self):
        with self._choice():
            with self._option():
                self._multiset_term_()
            with self._option():
                self._multiset_value_expression_()
                self._token('MULTISET')
                self._token('UNION')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                self._multiset_term_()
            with self._option():
                self._multiset_value_expression_()
                self._token('MULTISET')
                self._token('EXCEPT')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                self._multiset_term_()
            self._error('no available options')

    @graken
    def _multiset_term_(self):
        with self._choice():
            with self._option():
                self._multiset_primary_()
            with self._option():
                self._multiset_term_()
                self._token('MULTISET')
                self._token('INTERSECT')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                self._multiset_primary_()
            self._error('no available options')

    @graken
    def _multiset_primary_(self):
        with self._choice():
            with self._option():
                self._multiset_value_function_()
            with self._option():
                self._value_expression_primary_()
            self._error('no available options')

    @graken
    def _multiset_value_function_(self):
        self._multiset_set_function_()

    @graken
    def _multiset_set_function_(self):
        self._token('SET')
        self._token('(')
        self._multiset_value_expression_()
        self._token(')')

    @graken
    def _multiset_value_constructor_(self):
        with self._choice():
            with self._option():
                self._multiset_value_constructor_by_enumeration_()
            with self._option():
                self._multiset_value_constructor_by_query_()
            with self._option():
                self._table_value_constructor_by_query_()
            self._error('no available options')

    @graken
    def _multiset_value_constructor_by_enumeration_(self):
        self._token('MULTISET')
        self._left_bracket_or_trigraph_()
        self._multiset_element_list_()
        self._right_bracket_or_trigraph_()

    @graken
    def _multiset_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._multiset_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _multiset_element_(self):
        self._value_expression_()

    @graken
    def _multiset_value_constructor_by_query_(self):
        self._token('MULTISET')
        self._token('(')
        self._query_expression_()
        self._token(')')

    @graken
    def _table_value_constructor_by_query_(self):
        self._token('TABLE')
        self._token('(')
        self._query_expression_()
        self._token(')')

    @graken
    def _row_value_constructor_(self):
        with self._choice():
            with self._option():
                self._common_value_expression_()
            with self._option():
                self._boolean_value_expression_()
            with self._option():
                self._explicit_row_value_constructor_()
            self._error('no available options')

    @graken
    def _explicit_row_value_constructor_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._row_value_constructor_element_()
                self._token(',')
                self._row_value_constructor_element_list_()
                self._token(')')
            with self._option():
                self._token('ROW')
                self._token('(')
                self._row_value_constructor_element_list_()
                self._token(')')
            with self._option():
                self._subquery_()
            self._error('no available options')

    @graken
    def _row_value_constructor_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._row_value_constructor_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _row_value_constructor_element_(self):
        self._value_expression_()

    @graken
    def _contextually_typed_row_value_constructor_(self):
        with self._choice():
            with self._option():
                self._common_value_expression_()
            with self._option():
                self._boolean_value_expression_()
            with self._option():
                self._contextually_typed_value_specification_()
            with self._option():
                self._token('(')
                self._contextually_typed_row_value_constructor_element_()
                self._token(',')
                self._contextually_typed_row_value_constructor_element_list_()
                self._token(')')
            with self._option():
                self._token('ROW')
                self._token('(')
                self._contextually_typed_row_value_constructor_element_list_()
                self._token(')')
            self._error('no available options')

    @graken
    def _contextually_typed_row_value_constructor_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._contextually_typed_row_value_constructor_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _contextually_typed_row_value_constructor_element_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._contextually_typed_value_specification_()
            self._error('no available options')

    @graken
    def _row_value_constructor_predicand_(self):
        with self._choice():
            with self._option():
                self._common_value_expression_()
            with self._option():
                self._boolean_predicand_()
            with self._option():
                self._explicit_row_value_constructor_()
            self._error('no available options')

    @graken
    def _row_value_expression_(self):
        with self._choice():
            with self._option():
                self._row_value_special_case_()
            with self._option():
                self._explicit_row_value_constructor_()
            self._error('no available options')

    @graken
    def _table_row_value_expression_(self):
        with self._choice():
            with self._option():
                self._row_value_special_case_()
            with self._option():
                self._row_value_constructor_()
            self._error('no available options')

    @graken
    def _contextually_typed_row_value_expression_(self):
        with self._choice():
            with self._option():
                self._row_value_special_case_()
            with self._option():
                self._contextually_typed_row_value_constructor_()
            self._error('no available options')

    @graken
    def _row_value_predicand_(self):
        with self._choice():
            with self._option():
                self._row_value_special_case_()
            with self._option():
                self._row_value_constructor_predicand_()
            self._error('no available options')

    @graken
    def _row_value_special_case_(self):
        self._nonparenthesized_value_expression_primary_()

    @graken
    def _table_value_constructor_(self):
        self._token('VALUES')
        self._row_value_expression_list_()

    @graken
    def _row_value_expression_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._table_row_value_expression_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _contextually_typed_table_value_constructor_(self):
        self._token('VALUES')
        self._contextually_typed_row_value_expression_list_()

    @graken
    def _contextually_typed_row_value_expression_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._contextually_typed_row_value_expression_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _table_expression_(self):
        self._from_clause_()
        with self._optional():
            self._where_clause_()
        with self._optional():
            self._group_by_clause_()
        with self._optional():
            self._having_clause_()
        with self._optional():
            self._window_clause_()

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
        self._table_primary_or_joined_table_()
        with self._optional():
            self._sample_clause_()

    @graken
    def _table_primary_or_joined_table_(self):
        with self._choice():
            with self._option():
                self._table_primary_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _sample_clause_(self):
        self._token('TABLESAMPLE')
        self._sample_method_()
        self._token('(')
        self._sample_percentage_()
        self._token(')')
        with self._optional():
            self._repeatable_clause_()

    @graken
    def _sample_method_(self):
        with self._choice():
            with self._option():
                self._token('BERNOULLI')
            with self._option():
                self._token('SYSTEM')
            self._error('expecting one of: BERNOULLI SYSTEM')

    @graken
    def _repeatable_clause_(self):
        self._token('REPEATABLE')
        self._token('(')
        self._repeat_argument_()
        self._token(')')

    @graken
    def _sample_percentage_(self):
        self._numeric_value_expression_()

    @graken
    def _repeat_argument_(self):
        self._numeric_value_expression_()

    @graken
    def _table_primary_(self):
        with self._choice():
            with self._option():
                self._table_or_query_name_()
                with self._optional():
                    with self._optional():
                        self._token('AS')
                    self._correlation_name_()
                    with self._optional():
                        self._token('(')
                        self._column_name_list_()
                        self._token(')')
            with self._option():
                self._subquery_()
                with self._optional():
                    self._token('AS')
                self._correlation_name_()
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._lateral_derived_table_()
                with self._optional():
                    self._token('AS')
                self._correlation_name_()
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._collection_derived_table_()
                with self._optional():
                    self._token('AS')
                self._correlation_name_()
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._table_function_derived_table_()
                with self._optional():
                    self._token('AS')
                self._correlation_name_()
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._only_spec_()
                with self._optional():
                    with self._optional():
                        self._token('AS')
                    self._correlation_name_()
                    with self._optional():
                        self._token('(')
                        self._column_name_list_()
                        self._token(')')
            with self._option():
                self._token('(')
                self._joined_table_()
                self._token(')')
            self._error('no available options')

    @graken
    def _only_spec_(self):
        self._token('ONLY')
        self._token('(')
        self._table_or_query_name_()
        self._token(')')

    @graken
    def _lateral_derived_table_(self):
        self._token('LATERAL')
        self._subquery_()

    @graken
    def _collection_derived_table_(self):
        self._token('UNNEST')
        self._token('(')
        self._collection_value_expression_()
        self._token(')')
        with self._optional():
            self._token('WITH')
            self._token('ORDINALITY')

    @graken
    def _table_function_derived_table_(self):
        self._token('TABLE')
        self._token('(')
        self._collection_value_expression_()
        self._token(')')

    @graken
    def _table_or_query_name_(self):
        with self._choice():
            with self._option():
                self._table_name_()
            with self._option():
                self._query_name_()
            self._error('no available options')

    @graken
    def _column_name_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._column_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _joined_table_(self):
        with self._choice():
            with self._option():
                self._cross_join_()
            with self._option():
                self._qualified_join_()
            with self._option():
                self._natural_join_()
            with self._option():
                self._union_join_()
            self._error('no available options')

    @graken
    def _cross_join_(self):
        self._table_reference_()
        self._token('CROSS')
        self._token('JOIN')
        self._table_primary_()

    @graken
    def _qualified_join_(self):
        self._table_reference_()
        with self._optional():
            self._join_type_()
        self._token('JOIN')
        self._table_reference_()
        self._join_specification_()

    @graken
    def _natural_join_(self):
        self._table_reference_()
        self._token('NATURAL')
        with self._optional():
            self._join_type_()
        self._token('JOIN')
        self._table_primary_()

    @graken
    def _union_join_(self):
        self._table_reference_()
        self._token('UNION')
        self._token('JOIN')
        self._table_primary_()

    @graken
    def _join_specification_(self):
        with self._choice():
            with self._option():
                self._join_condition_()
            with self._option():
                self._named_columns_join_()
            self._error('no available options')

    @graken
    def _join_condition_(self):
        self._token('ON')
        self._search_condition_()

    @graken
    def _named_columns_join_(self):
        self._token('USING')
        self._token('(')
        self._column_name_list_()
        self._token(')')

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
        self._search_condition_()

    @graken
    def _group_by_clause_(self):
        self._token('GROUP')
        self._token('BY')
        with self._optional():
            self._set_quantifier_()
        self._grouping_element_list_()

    @graken
    def _grouping_element_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._grouping_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _grouping_element_(self):
        with self._choice():
            with self._option():
                self._ordinary_grouping_set_()
            with self._option():
                self._rollup_list_()
            with self._option():
                self._cube_list_()
            with self._option():
                self._grouping_sets_specification_()
            with self._option():
                self._empty_grouping_set_()
            self._error('no available options')

    @graken
    def _ordinary_grouping_set_(self):
        with self._choice():
            with self._option():
                self._grouping_column_reference_()
            with self._option():
                self._token('(')
                self._grouping_column_reference_list_()
                self._token(')')
            self._error('no available options')

    @graken
    def _grouping_column_reference_(self):
        self._column_reference_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _grouping_column_reference_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._grouping_column_reference_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _rollup_list_(self):
        self._token('ROLLUP')
        self._token('(')
        self._ordinary_grouping_set_list_()
        self._token(')')

    @graken
    def _ordinary_grouping_set_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._ordinary_grouping_set_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _cube_list_(self):
        self._token('CUBE')
        self._token('(')
        self._ordinary_grouping_set_list_()
        self._token(')')

    @graken
    def _grouping_sets_specification_(self):
        self._token('GROUPING')
        self._token('SETS')
        self._token('(')
        self._grouping_set_list_()
        self._token(')')

    @graken
    def _grouping_set_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._grouping_set_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _grouping_set_(self):
        with self._choice():
            with self._option():
                self._ordinary_grouping_set_()
            with self._option():
                self._rollup_list_()
            with self._option():
                self._cube_list_()
            with self._option():
                self._grouping_sets_specification_()
            with self._option():
                self._empty_grouping_set_()
            self._error('no available options')

    @graken
    def _empty_grouping_set_(self):
        self._token('(')
        self._token(')')

    @graken
    def _having_clause_(self):
        self._token('HAVING')
        self._search_condition_()

    @graken
    def _window_clause_(self):
        self._token('WINDOW')
        self._window_definition_list_()

    @graken
    def _window_definition_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._window_definition_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _window_definition_(self):
        self._new_window_name_()
        self._token('AS')
        self._window_specification_()

    @graken
    def _new_window_name_(self):
        self._window_name_()

    @graken
    def _window_specification_(self):
        self._token('(')
        self._window_specification_details_()
        self._token(')')

    @graken
    def _window_specification_details_(self):
        with self._optional():
            self._existing_window_name_()
        with self._optional():
            self._window_partition_clause_()
        with self._optional():
            self._window_order_clause_()
        with self._optional():
            self._window_frame_clause_()

    @graken
    def _existing_window_name_(self):
        self._window_name_()

    @graken
    def _window_partition_clause_(self):
        self._token('PARTITION')
        self._token('BY')
        self._window_partition_column_reference_list_()

    @graken
    def _window_partition_column_reference_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._window_partition_column_reference_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _window_partition_column_reference_(self):
        self._column_reference_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _window_order_clause_(self):
        self._token('ORDER')
        self._token('BY')
        self._sort_specification_list_()

    @graken
    def _window_frame_clause_(self):
        self._window_frame_units_()
        self._window_frame_extent_()
        with self._optional():
            self._window_frame_exclusion_()

    @graken
    def _window_frame_units_(self):
        with self._choice():
            with self._option():
                self._token('ROWS')
            with self._option():
                self._token('RANGE')
            self._error('expecting one of: RANGE ROWS')

    @graken
    def _window_frame_extent_(self):
        with self._choice():
            with self._option():
                self._window_frame_start_()
            with self._option():
                self._window_frame_between_()
            self._error('no available options')

    @graken
    def _window_frame_start_(self):
        with self._choice():
            with self._option():
                self._token('UNBOUNDED')
                self._token('PRECEDING')
            with self._option():
                self._window_frame_preceding_()
            with self._option():
                self._token('CURRENT')
                self._token('ROW')
            self._error('expecting one of: CURRENT UNBOUNDED')

    @graken
    def _window_frame_preceding_(self):
        self._unsigned_value_specification_()
        self._token('PRECEDING')

    @graken
    def _window_frame_between_(self):
        self._token('BETWEEN')
        self._window_frame_bound_()
        self._token('AND')
        self._window_frame_bound_()

    @graken
    def _window_frame_bound_(self):
        with self._choice():
            with self._option():
                self._window_frame_start_()
            with self._option():
                self._token('UNBOUNDED')
                self._token('FOLLOWING')
            with self._option():
                self._window_frame_following_()
            self._error('expecting one of: UNBOUNDED')

    @graken
    def _window_frame_following_(self):
        self._unsigned_value_specification_()
        self._token('FOLLOWING')

    @graken
    def _window_frame_exclusion_(self):
        with self._choice():
            with self._option():
                self._token('EXCLUDE')
                self._token('CURRENT')
                self._token('ROW')
            with self._option():
                self._token('EXCLUDE')
                self._token('GROUP')
            with self._option():
                self._token('EXCLUDE')
                self._token('TIES')
            with self._option():
                self._token('EXCLUDE')
                self._token('NO')
                self._token('OTHERS')
            self._error('expecting one of: EXCLUDE')

    @graken
    def _query_specification_(self):
        self._token('SELECT')
        with self._optional():
            self._set_quantifier_()
        self._select_list_()
        self._table_expression_()

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
                self._derived_column_()
            with self._option():
                self._qualified_asterisk_()
            self._error('no available options')

    @graken
    def _qualified_asterisk_(self):
        with self._choice():
            with self._option():
                self._asterisked_identifier_chain_()
                self._token('.')
                self._token('*')
            with self._option():
                self._all_fields_reference_()
            self._error('no available options')

    @graken
    def _asterisked_identifier_chain_(self):
        def sep0():
            self._token('.')

        def block0():
            self._asterisked_identifier_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _asterisked_identifier_(self):
        self._identifier_()

    @graken
    def _derived_column_(self):
        self._value_expression_()
        with self._optional():
            self._as_clause_()

    @graken
    def _as_clause_(self):
        with self._optional():
            self._token('AS')
        self._column_name_()

    @graken
    def _all_fields_reference_(self):
        self._value_expression_primary_()
        self._token('.')
        self._token('*')
        with self._optional():
            self._token('AS')
            self._token('(')
            self._column_name_list_()
            self._token(')')

    @graken
    def _query_expression_(self):
        with self._optional():
            self._with_clause_()
        self._query_expression_body_()

    @graken
    def _with_clause_(self):
        self._token('WITH')
        with self._optional():
            self._token('RECURSIVE')
        self._with_list_()

    @graken
    def _with_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._with_list_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _with_list_element_(self):
        self._query_name_()
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')
        self._token('AS')
        self._token('(')
        self._query_expression_()
        self._token(')')
        with self._optional():
            self._search_or_cycle_clause_()

    @graken
    def _query_expression_body_(self):
        with self._choice():
            with self._option():
                self._non_join_query_expression_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _non_join_query_expression_(self):
        with self._choice():
            with self._option():
                self._non_join_query_term_()
            with self._option():
                self._query_expression_body_()
                self._token('UNION')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                with self._optional():
                    self._corresponding_spec_()
                self._query_term_()
            with self._option():
                self._query_expression_body_()
                self._token('EXCEPT')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                with self._optional():
                    self._corresponding_spec_()
                self._query_term_()
            self._error('no available options')

    @graken
    def _query_term_(self):
        with self._choice():
            with self._option():
                self._non_join_query_term_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _non_join_query_term_(self):
        with self._choice():
            with self._option():
                self._non_join_query_primary_()
            with self._option():
                self._query_term_()
                self._token('INTERSECT')
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('ALL')
                        with self._option():
                            self._token('DISTINCT')
                        self._error('expecting one of: ALL DISTINCT')
                with self._optional():
                    self._corresponding_spec_()
                self._query_primary_()
            self._error('no available options')

    @graken
    def _query_primary_(self):
        with self._choice():
            with self._option():
                self._non_join_query_primary_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _non_join_query_primary_(self):
        with self._choice():
            with self._option():
                self._simple_table_()
            with self._option():
                self._token('(')
                self._non_join_query_expression_()
                self._token(')')
            self._error('no available options')

    @graken
    def _simple_table_(self):
        with self._choice():
            with self._option():
                self._query_specification_()
            with self._option():
                self._table_value_constructor_()
            with self._option():
                self._explicit_table_()
            self._error('no available options')

    @graken
    def _explicit_table_(self):
        self._token('TABLE')
        self._table_or_query_name_()

    @graken
    def _corresponding_spec_(self):
        self._token('CORRESPONDING')
        with self._optional():
            self._token('BY')
            self._token('(')
            self._column_name_list_()
            self._token(')')

    @graken
    def _search_or_cycle_clause_(self):
        with self._choice():
            with self._option():
                self._search_clause_()
            with self._option():
                self._cycle_clause_()
            with self._option():
                self._search_clause_()
                self._cycle_clause_()
            self._error('no available options')

    @graken
    def _search_clause_(self):
        self._token('SEARCH')
        self._recursive_search_order_()
        self._token('SET')
        self._column_name_()

    @graken
    def _recursive_search_order_(self):
        with self._choice():
            with self._option():
                self._token('DEPTH')
                self._token('FIRST')
                self._token('BY')
                self._sort_specification_list_()
            with self._option():
                self._token('BREADTH')
                self._token('FIRST')
                self._token('BY')
                self._sort_specification_list_()
            self._error('no available options')

    @graken
    def _cycle_clause_(self):
        self._token('CYCLE')
        self._cycle_column_list_()
        self._token('SET')
        self._column_name_()
        self._token('TO')
        self._cycle_mark_value_()
        self._token('DEFAULT')
        self._non_cycle_mark_value_()
        self._token('USING')
        self._column_name_()

    @graken
    def _cycle_column_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._column_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _cycle_mark_value_(self):
        self._value_expression_()

    @graken
    def _non_cycle_mark_value_(self):
        self._value_expression_()

    @graken
    def _subquery_(self):
        self._token('(')
        self._query_expression_()
        self._token(')')

    @graken
    def _predicate_(self):
        with self._choice():
            with self._option():
                self._comparison_predicate_()
            with self._option():
                self._between_predicate_()
            with self._option():
                self._in_predicate_()
            with self._option():
                self._like_predicate_()
            with self._option():
                self._similar_predicate_()
            with self._option():
                self._null_predicate_()
            with self._option():
                self._quantified_comparison_predicate_()
            with self._option():
                self._exists_predicate_()
            with self._option():
                self._unique_predicate_()
            with self._option():
                self._normalized_predicate_()
            with self._option():
                self._match_predicate_()
            with self._option():
                self._overlaps_predicate_()
            with self._option():
                self._distinct_predicate_()
            with self._option():
                self._member_predicate_()
            with self._option():
                self._submultiset_predicate_()
            with self._option():
                self._set_predicate_()
            with self._option():
                self._type_predicate_()
            self._error('no available options')

    @graken
    def _comparison_predicate_(self):
        self._row_value_predicand_()
        self._comp_op_()
        self._row_value_predicand_()

    @graken
    def _comp_op_(self):
        with self._choice():
            with self._option():
                self._token('=')
            with self._option():
                self._token('<>')
            with self._option():
                self._token('<')
            with self._option():
                self._token('>')
            with self._option():
                self._token('<=')
            with self._option():
                self._token('>=')
            self._error('expecting one of: < <= <> = > >=')

    @graken
    def _between_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('BETWEEN')
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('ASYMMETRIC')
                with self._option():
                    self._token('SYMMETRIC')
                self._error('expecting one of: ASYMMETRIC SYMMETRIC')
        self._row_value_predicand_()
        self._token('AND')
        self._row_value_predicand_()

    @graken
    def _in_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('IN')
        self._in_predicate_value_()

    @graken
    def _in_predicate_value_(self):
        with self._choice():
            with self._option():
                self._subquery_()
            with self._option():
                self._token('(')
                self._in_value_list_()
                self._token(')')
            self._error('no available options')

    @graken
    def _in_value_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._row_value_expression_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _like_predicate_(self):
        with self._choice():
            with self._option():
                self._character_like_predicate_()
            with self._option():
                self._octet_like_predicate_()
            self._error('no available options')

    @graken
    def _character_like_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('LIKE')
        self._character_pattern_()
        with self._optional():
            self._token('ESCAPE')
            self._escape_character_()

    @graken
    def _character_pattern_(self):
        self._character_value_expression_()

    @graken
    def _escape_character_(self):
        self._character_value_expression_()

    @graken
    def _octet_like_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('LIKE')
        self._octet_pattern_()
        with self._optional():
            self._token('ESCAPE')
            self._escape_octet_()

    @graken
    def _octet_pattern_(self):
        self._blob_value_expression_()

    @graken
    def _escape_octet_(self):
        self._blob_value_expression_()

    @graken
    def _similar_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('SIMILAR')
        self._token('TO')
        self._similar_pattern_()
        with self._optional():
            self._token('ESCAPE')
            self._escape_character_()

    @graken
    def _similar_pattern_(self):
        self._character_value_expression_()

    @graken
    def _regular_expression_(self):
        with self._optional():
            self._regular_expression_()
            self._token('|')
        self._regular_term_()

    @graken
    def _regular_term_(self):
        with self._optional():
            self._regular_term_()
        self._regular_factor_()

    @graken
    def _regular_factor_(self):
        with self._choice():
            with self._option():
                self._regular_primary_()
            with self._option():
                self._regular_primary_()
                self._token('*')
            with self._option():
                self._regular_primary_()
                self._token('+')
            with self._option():
                self._regular_primary_()
                self._token('?')
            with self._option():
                self._regular_primary_()
                self._repeat_factor_()
            self._error('no available options')

    @graken
    def _repeat_factor_(self):
        self._token('{')
        self._integer_()
        with self._optional():
            self._upper_limit_()
        self._token('}')

    @graken
    def _upper_limit_(self):
        self._token(',')
        with self._optional():
            self._integer_()

    @graken
    def _regular_primary_(self):
        with self._choice():
            with self._option():
                self._character_specifier_()
            with self._option():
                self._token('%')
            with self._option():
                self._regular_character_set_()
            with self._option():
                self._token('(')
                self._regular_expression_()
                self._token(')')
            self._error('expecting one of: %')

    @graken
    def _character_specifier_(self):
        with self._choice():
            with self._option():
                self._non_escaped_character_()
            with self._option():
                self._escaped_character_()
            self._error('no available options')

    @graken
    def _non_escaped_character_(self):
        self._letter_()

    @graken
    def _escaped_character_(self):
        self._token('@r')

    @graken
    def _regular_character_set_(self):
        with self._choice():
            with self._option():
                self._token('_')
            with self._option():
                self._token('[')

                def block0():
                    self._character_enumeration_()

                self._positive_closure(block0)
                self._token(']')
            with self._option():
                self._token('[')
                self._token('^')

                def block1():
                    self._character_enumeration_()

                self._positive_closure(block1)
                self._token(']')
            with self._option():
                self._token('[')

                def block2():
                    self._character_enumeration_()

                self._positive_closure(block2)
                self._token('^')

                def block3():
                    self._character_enumeration_()

                self._positive_closure(block3)
                self._token(']')
            self._error('expecting one of: _')

    @graken
    def _character_enumeration_(self):
        with self._choice():
            with self._option():
                self._character_specifier_()
            with self._option():
                self._character_specifier_()
                self._token('-')
                self._character_specifier_()
            with self._option():
                self._token('[')
                self._token(':')
                self._regular_character_set_identifier_()
                self._token(':')
                self._token(']')
            self._error('no available options')

    @graken
    def _regular_character_set_identifier_(self):
        self._identifier_()

    @graken
    def _null_predicate_(self):
        self._row_value_predicand_()
        self._token('IS')
        with self._optional():
            self._token('NOT')
        self._token('NULL')

    @graken
    def _quantified_comparison_predicate_(self):
        self._row_value_predicand_()
        self._comp_op_()
        self._quantifier_()
        self._subquery_()

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
    def _exists_predicate_(self):
        self._token('EXISTS')
        self._subquery_()

    @graken
    def _unique_predicate_(self):
        self._token('UNIQUE')
        self._subquery_()

    @graken
    def _normalized_predicate_(self):
        self._string_value_expression_()
        self._token('IS')
        with self._optional():
            self._token('NOT')
        self._token('NORMALIZED')

    @graken
    def _match_predicate_(self):
        self._row_value_predicand_()
        self._token('MATCH')
        with self._optional():
            self._token('UNIQUE')
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('SIMPLE')
                with self._option():
                    self._token('PARTIAL')
                with self._option():
                    self._token('FULL')
                self._error('expecting one of: FULL PARTIAL SIMPLE')
        self._subquery_()

    @graken
    def _overlaps_predicate_(self):
        self._row_value_predicand_()
        self._token('OVERLAPS')
        self._row_value_predicand_()

    @graken
    def _distinct_predicate_(self):
        self._row_value_predicand_()
        self._token('IS')
        self._token('DISTINCT')
        self._token('FROM')
        self._row_value_predicand_()

    @graken
    def _member_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('MEMBER')
        with self._optional():
            self._token('OF')
        self._multiset_value_expression_()

    @graken
    def _submultiset_predicate_(self):
        self._row_value_predicand_()
        with self._optional():
            self._token('NOT')
        self._token('SUBMULTISET')
        with self._optional():
            self._token('OF')
        self._multiset_value_expression_()

    @graken
    def _set_predicate_(self):
        self._row_value_predicand_()
        self._token('IS')
        with self._optional():
            self._token('NOT')
        self._token('A')
        self._token('SET')

    @graken
    def _type_predicate_(self):
        self._row_value_predicand_()
        self._token('IS')
        with self._optional():
            self._token('NOT')
        self._token('OF')
        self._token('(')
        self._type_list_()
        self._token(')')

    @graken
    def _type_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._user_defined_type_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _user_defined_type_specification_(self):
        with self._choice():
            with self._option():
                self._inclusive_user_defined_type_specification_()
            with self._option():
                self._exclusive_user_defined_type_specification_()
            self._error('no available options')

    @graken
    def _inclusive_user_defined_type_specification_(self):
        self._path_resolved_user_defined_type_name_()

    @graken
    def _exclusive_user_defined_type_specification_(self):
        self._token('ONLY')
        self._path_resolved_user_defined_type_name_()

    @graken
    def _search_condition_(self):
        self._boolean_value_expression_()

    @graken
    def _interval_qualifier_(self):
        with self._choice():
            with self._option():
                self._start_field_()
                self._token('TO')
                self._end_field_()
            with self._option():
                self._single_datetime_field_()
            self._error('no available options')

    @graken
    def _start_field_(self):
        self._non_second_primary_datetime_field_()
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _end_field_(self):
        with self._choice():
            with self._option():
                self._non_second_primary_datetime_field_()
            with self._option():
                self._token('SECOND')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            self._error('expecting one of: SECOND')

    @graken
    def _single_datetime_field_(self):
        with self._choice():
            with self._option():
                self._non_second_primary_datetime_field_()
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('SECOND')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    with self._optional():
                        self._token(',')
                        self._integer_()
                    self._token(')')
            self._error('expecting one of: SECOND')

    @graken
    def _primary_datetime_field_(self):
        with self._choice():
            with self._option():
                self._non_second_primary_datetime_field_()
            with self._option():
                self._token('SECOND')
            self._error('expecting one of: SECOND')

    @graken
    def _non_second_primary_datetime_field_(self):
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
            self._error('expecting one of: DAY HOUR MINUTE MONTH YEAR')

    @graken
    def _language_clause_(self):
        self._token('LANGUAGE')
        self._language_name_()

    @graken
    def _language_name_(self):
        with self._choice():
            with self._option():
                self._token('ADA')
            with self._option():
                self._token('C')
            with self._option():
                self._token('COBOL')
            with self._option():
                self._token('FORTRAN')
            with self._option():
                self._token('MUMPS')
            with self._option():
                self._token('PASCAL')
            with self._option():
                self._token('PLI')
            with self._option():
                self._token('SQL')
            self._error('expecting one of: ADA C COBOL FORTRAN MUMPS PASCAL '
                        'PLI SQL')

    @graken
    def _path_specification_(self):
        self._token('PATH')
        self._schema_name_list_()

    @graken
    def _schema_name_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._schema_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _routine_invocation_(self):
        self._routine_name_()
        self._sql_argument_list_()

    @graken
    def _routine_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _sql_argument_list_(self):
        self._token('(')
        with self._optional():
            def sep0():
                self._token(',')

            def block0():
                self._sql_argument_()

            self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _sql_argument_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._generalized_expression_()
            with self._option():
                self._target_specification_()
            self._error('no available options')

    @graken
    def _generalized_expression_(self):
        self._value_expression_()
        self._token('AS')
        self._path_resolved_user_defined_type_name_()

    @graken
    def _specific_routine_designator_(self):
        with self._choice():
            with self._option():
                self._token('SPECIFIC')
                self._routine_type_()
                self._specific_name_()
            with self._option():
                self._routine_type_()
                self._member_name_()
                with self._optional():
                    self._token('FOR')
                    self._schema_resolved_user_defined_type_name_()
            self._error('no available options')

    @graken
    def _routine_type_(self):
        with self._choice():
            with self._option():
                self._token('ROUTINE')
            with self._option():
                self._token('FUNCTION')
            with self._option():
                self._token('PROCEDURE')
            with self._option():
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('INSTANCE')
                        with self._option():
                            self._token('STATIC')
                        with self._option():
                            self._token('CONSTRUCTOR')
                        self._error('expecting one of: CONSTRUCTOR INSTANCE '
                                    'STATIC')
                self._token('METHOD')
            self._error('expecting one of: CONSTRUCTOR FUNCTION INSTANCE '
                        'METHOD PROCEDURE ROUTINE STATIC')

    @graken
    def _member_name_(self):
        self._member_name_alternatives_()
        with self._optional():
            self._data_type_list_()

    @graken
    def _member_name_alternatives_(self):
        with self._choice():
            with self._option():
                self._schema_qualified_routine_name_()
            with self._option():
                self._method_name_()
            self._error('no available options')

    @graken
    def _data_type_list_(self):
        self._token('(')
        with self._optional():
            def sep0():
                self._token(',')

            def block0():
                self._data_type_()

            self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _collate_clause_(self):
        self._token('COLLATE')
        self._collation_name_()

    @graken
    def _constraint_name_definition_(self):
        self._token('CONSTRAINT')
        self._constraint_name_()

    @graken
    def _constraint_characteristics_(self):
        with self._choice():
            with self._option():
                self._constraint_check_time_()
                with self._optional():
                    with self._optional():
                        self._token('NOT')
                    self._token('DEFERRABLE')
            with self._option():
                with self._optional():
                    self._token('NOT')
                self._token('DEFERRABLE')
                with self._optional():
                    self._constraint_check_time_()
            self._error('expecting one of: DEFERRABLE NOT')

    @graken
    def _constraint_check_time_(self):
        with self._choice():
            with self._option():
                self._token('INITIALLY')
                self._token('DEFERRED')
            with self._option():
                self._token('INITIALLY')
                self._token('IMMEDIATE')
            self._error('expecting one of: INITIALLY')

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
                self._general_set_function_()
                with self._optional():
                    self._filter_clause_()
            with self._option():
                self._binary_set_function_()
                with self._optional():
                    self._filter_clause_()
            with self._option():
                self._ordered_set_function_()
                with self._optional():
                    self._filter_clause_()
            self._error('expecting one of: COUNT')

    @graken
    def _general_set_function_(self):
        self._set_computational_operation_()
        self._token('(')
        with self._optional():
            self._set_quantifier_()
        self._value_expression_()
        self._token(')')

    @graken
    def _set_computational_operation_(self):
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
                self._token('SOME')
            with self._option():
                self._token('COUNT')
            with self._option():
                self._token('STDDEV_POP')
            with self._option():
                self._token('STDDEV_SAMP')
            with self._option():
                self._token('VAR_SAMP')
            with self._option():
                self._token('VAR_POP')
            with self._option():
                self._token('COLLECT')
            with self._option():
                self._token('FUSION')
            with self._option():
                self._token('INTERSECTION')
            self._error('expecting one of: ANY AVG COLLECT COUNT EVERY FUSION '
                        'INTERSECTION MAX MIN SOME STDDEV_POP STDDEV_SAMP SUM '
                        'VAR_POP VAR_SAMP')

    @graken
    def _set_quantifier_(self):
        with self._choice():
            with self._option():
                self._token('DISTINCT')
            with self._option():
                self._token('ALL')
            self._error('expecting one of: ALL DISTINCT')

    @graken
    def _filter_clause_(self):
        self._token('FILTER')
        self._token('(')
        self._token('WHERE')
        self._search_condition_()
        self._token(')')

    @graken
    def _binary_set_function_(self):
        self._binary_set_function_type_()
        self._token('(')
        self._dependent_variable_expression_()
        self._token(',')
        self._independent_variable_expression_()
        self._token(')')

    @graken
    def _binary_set_function_type_(self):
        with self._choice():
            with self._option():
                self._token('COVAR_POP')
            with self._option():
                self._token('COVAR_SAMP')
            with self._option():
                self._token('CORR')
            with self._option():
                self._token('REGR_SLOPE')
            with self._option():
                self._token('REGR_INTERCEPT')
            with self._option():
                self._token('REGR_COUNT')
            with self._option():
                self._token('REGR_R2')
            with self._option():
                self._token('REGR_AVGX')
            with self._option():
                self._token('REGR_AVGY')
            with self._option():
                self._token('REGR_SXX')
            with self._option():
                self._token('REGR_SYY')
            with self._option():
                self._token('REGR_SXY')
            self._error('expecting one of: CORR COVAR_POP COVAR_SAMP '
                        'REGR_AVGX REGR_AVGY REGR_COUNT REGR_INTERCEPT '
                        'REGR_R2 REGR_SLOPE REGR_SXX REGR_SXY REGR_SYY')

    @graken
    def _dependent_variable_expression_(self):
        self._numeric_value_expression_()

    @graken
    def _independent_variable_expression_(self):
        self._numeric_value_expression_()

    @graken
    def _ordered_set_function_(self):
        with self._choice():
            with self._option():
                self._hypothetical_set_function_()
            with self._option():
                self._inverse_distribution_function_()
            self._error('no available options')

    @graken
    def _hypothetical_set_function_(self):
        self._rank_function_type_()
        self._token('(')
        self._hypothetical_set_function_value_expression_list_()
        self._token(')')
        self._within_group_specification_()

    @graken
    def _within_group_specification_(self):
        self._token('WITHIN')
        self._token('GROUP')
        self._token('(')
        self._token('ORDER')
        self._token('BY')
        self._sort_specification_list_()
        self._token(')')

    @graken
    def _hypothetical_set_function_value_expression_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._value_expression_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _inverse_distribution_function_(self):
        self._inverse_distribution_function_type_()
        self._token('(')
        self._numeric_value_expression_()
        self._token(')')
        self._within_group_specification_()

    @graken
    def _inverse_distribution_function_type_(self):
        with self._choice():
            with self._option():
                self._token('PERCENTILE_CONT')
            with self._option():
                self._token('PERCENTILE_DISC')
            self._error('expecting one of: PERCENTILE_CONT PERCENTILE_DISC')

    @graken
    def _sort_specification_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._sort_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _sort_specification_(self):
        self._sort_key_()
        with self._optional():
            self._ordering_specification_()
        with self._optional():
            self._null_ordering_()

    @graken
    def _sort_key_(self):
        self._value_expression_()

    @graken
    def _ordering_specification_(self):
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
    def _schema_definition_(self):
        self._token('CREATE')
        self._token('SCHEMA')
        self._schema_name_clause_()
        with self._optional():
            self._schema_character_set_or_path_()
        with self._optional():
            def block0():
                self._schema_element_()

            self._positive_closure(block0)

    @graken
    def _schema_character_set_or_path_(self):
        with self._choice():
            with self._option():
                self._schema_character_set_specification_()
            with self._option():
                self._schema_path_specification_()
            with self._option():
                self._schema_character_set_specification_()
                self._schema_path_specification_()
            with self._option():
                self._schema_path_specification_()
                self._schema_character_set_specification_()
            self._error('no available options')

    @graken
    def _schema_name_clause_(self):
        with self._choice():
            with self._option():
                self._schema_name_()
            with self._option():
                self._token('AUTHORIZATION')
                self._schema_authorization_identifier_()
            with self._option():
                self._schema_name_()
                self._token('AUTHORIZATION')
                self._schema_authorization_identifier_()
            self._error('no available options')

    @graken
    def _schema_authorization_identifier_(self):
        self._authorization_identifier_()

    @graken
    def _schema_character_set_specification_(self):
        self._token('DEFAULT')
        self._token('CHARACTER')
        self._token('SET')
        self._character_set_name_()

    @graken
    def _schema_path_specification_(self):
        self._path_specification_()

    @graken
    def _schema_element_(self):
        with self._choice():
            with self._option():
                self._table_definition_()
            with self._option():
                self._view_definition_()
            with self._option():
                self._domain_definition_()
            with self._option():
                self._character_set_definition_()
            with self._option():
                self._collation_definition_()
            with self._option():
                self._transliteration_definition_()
            with self._option():
                self._assertion_definition_()
            with self._option():
                self._trigger_definition_()
            with self._option():
                self._user_defined_type_definition_()
            with self._option():
                self._user_defined_cast_definition_()
            with self._option():
                self._user_defined_ordering_definition_()
            with self._option():
                self._transform_definition_()
            with self._option():
                self._schema_routine_()
            with self._option():
                self._sequence_generator_definition_()
            with self._option():
                self._grant_statement_()
            with self._option():
                self._role_definition_()
            self._error('no available options')

    @graken
    def _drop_schema_statement_(self):
        self._token('DROP')
        self._token('SCHEMA')
        self._schema_name_()
        self._drop_behavior_()

    @graken
    def _drop_behavior_(self):
        with self._choice():
            with self._option():
                self._token('CASCADE')
            with self._option():
                self._token('RESTRICT')
            self._error('expecting one of: CASCADE RESTRICT')

    @graken
    def _table_definition_(self):
        self._token('CREATE')
        with self._optional():
            self._table_scope_()
        self._token('TABLE')
        self._table_name_()
        self._table_contents_source_()
        with self._optional():
            self._token('ON')
            self._token('COMMIT')
            self._table_commit_action_()
            self._token('ROWS')

    @graken
    def _table_contents_source_(self):
        with self._choice():
            with self._option():
                self._table_element_list_()
            with self._option():
                self._token('OF')
                self._path_resolved_user_defined_type_name_()
                with self._optional():
                    self._subtable_clause_()
                with self._optional():
                    self._table_element_list_()
            with self._option():
                self._as_subquery_clause_()
            self._error('no available options')

    @graken
    def _table_scope_(self):
        self._global_or_local_()
        self._token('TEMPORARY')

    @graken
    def _global_or_local_(self):
        with self._choice():
            with self._option():
                self._token('GLOBAL')
            with self._option():
                self._token('LOCAL')
            self._error('expecting one of: GLOBAL LOCAL')

    @graken
    def _table_commit_action_(self):
        with self._choice():
            with self._option():
                self._token('PRESERVE')
            with self._option():
                self._token('DELETE')
            self._error('expecting one of: DELETE PRESERVE')

    @graken
    def _table_element_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._table_element_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _table_element_(self):
        with self._choice():
            with self._option():
                self._column_definition_()
            with self._option():
                self._table_constraint_definition_()
            with self._option():
                self._like_clause_()
            with self._option():
                self._self_referencing_column_specification_()
            with self._option():
                self._column_options_()
            self._error('no available options')

    @graken
    def _self_referencing_column_specification_(self):
        self._token('REF')
        self._token('IS')
        self._column_name_()
        self._reference_generation_()

    @graken
    def _reference_generation_(self):
        with self._choice():
            with self._option():
                self._token('SYSTEM')
                self._token('GENERATED')
            with self._option():
                self._token('USER')
                self._token('GENERATED')
            with self._option():
                self._token('DERIVED')
            self._error('expecting one of: DERIVED SYSTEM USER')

    @graken
    def _column_options_(self):
        self._column_name_()
        self._token('WITH')
        self._token('OPTIONS')
        self._column_option_list_()

    @graken
    def _column_option_list_(self):
        with self._optional():
            self._scope_clause_()
        with self._optional():
            self._default_clause_()
        with self._optional():
            def block0():
                self._column_constraint_definition_()

            self._positive_closure(block0)

    @graken
    def _subtable_clause_(self):
        self._token('UNDER')
        self._table_name_()

    @graken
    def _like_clause_(self):
        self._token('LIKE')
        self._table_name_()
        with self._optional():
            self._like_options_()

    @graken
    def _like_options_(self):
        with self._choice():
            with self._option():
                self._identity_option_()
            with self._option():
                self._column_default_option_()
            self._error('no available options')

    @graken
    def _identity_option_(self):
        with self._choice():
            with self._option():
                self._token('INCLUDING')
                self._token('IDENTITY')
            with self._option():
                self._token('EXCLUDING')
                self._token('IDENTITY')
            self._error('expecting one of: EXCLUDING INCLUDING')

    @graken
    def _column_default_option_(self):
        with self._choice():
            with self._option():
                self._token('INCLUDING')
                self._token('DEFAULTS')
            with self._option():
                self._token('EXCLUDING')
                self._token('DEFAULTS')
            self._error('expecting one of: EXCLUDING INCLUDING')

    @graken
    def _as_subquery_clause_(self):
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')
        self._token('AS')
        self._subquery_()
        self._with_or_without_data_()

    @graken
    def _with_or_without_data_(self):
        self._token('WITH')
        with self._optional():
            self._token('NO')
        self._token('DATA')

    @graken
    def _column_definition_(self):
        self._column_name_()
        with self._optional():
            with self._choice():
                with self._option():
                    self._data_type_()
                with self._option():
                    self._domain_name_()
                self._error('no available options')
        with self._optional():
            self._reference_scope_check_()
        with self._optional():
            with self._choice():
                with self._option():
                    self._default_clause_()
                with self._option():
                    self._identity_column_specification_()
                with self._option():
                    self._generation_clause_()
                self._error('no available options')
        with self._optional():
            def block2():
                self._column_constraint_definition_()

            self._positive_closure(block2)
        with self._optional():
            self._collate_clause_()

    @graken
    def _column_constraint_definition_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._column_constraint_()
        with self._optional():
            self._constraint_characteristics_()

    @graken
    def _column_constraint_(self):
        with self._choice():
            with self._option():
                self._token('NOT')
                self._token('NULL')
            with self._option():
                self._unique_specification_()
            with self._option():
                self._references_specification_()
            with self._option():
                self._check_constraint_definition_()
            self._error('expecting one of: NOT')

    @graken
    def _reference_scope_check_(self):
        self._token('REFERENCES')
        self._token('ARE')
        with self._optional():
            self._token('NOT')
        self._token('CHECKED')
        with self._optional():
            self._token('ON')
            self._token('DELETE')
            self._reference_scope_check_action_()

    @graken
    def _reference_scope_check_action_(self):
        self._referential_action_()

    @graken
    def _identity_column_specification_(self):
        self._token('GENERATED')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('ALWAYS')
                with self._option():
                    self._token('BY')
                    self._token('DEFAULT')
                self._error('expecting one of: ALWAYS BY')
        self._token('AS')
        self._token('IDENTITY')
        with self._optional():
            self._token('(')
            self._common_sequence_generator_options_()
            self._token(')')

    @graken
    def _generation_clause_(self):
        self._token('GENERATED')
        self._token('ALWAYS')
        self._token('AS')
        self._generation_expression_()

    @graken
    def _generation_expression_(self):
        self._token('(')
        self._value_expression_()
        self._token(')')

    @graken
    def _default_clause_(self):
        self._token('DEFAULT')
        self._default_option_()

    @graken
    def _default_option_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._datetime_value_function_()
            with self._option():
                self._token('USER')
            with self._option():
                self._token('CURRENT_USER')
            with self._option():
                self._token('CURRENT_ROLE')
            with self._option():
                self._token('SESSION_USER')
            with self._option():
                self._token('SYSTEM_USER')
            with self._option():
                self._token('CURRENT_PATH')
            with self._option():
                self._implicitly_typed_value_specification_()
            self._error('expecting one of: CURRENT_PATH CURRENT_ROLE '
                        'CURRENT_USER SESSION_USER SYSTEM_USER USER')

    @graken
    def _table_constraint_definition_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._table_constraint_()
        with self._optional():
            self._constraint_characteristics_()

    @graken
    def _table_constraint_(self):
        with self._choice():
            with self._option():
                self._unique_constraint_definition_()
            with self._option():
                self._referential_constraint_definition_()
            with self._option():
                self._check_constraint_definition_()
            self._error('no available options')

    @graken
    def _unique_constraint_definition_(self):
        with self._choice():
            with self._option():
                self._unique_specification_()
                self._token('(')
                self._column_name_list_()
                self._token(')')
            with self._option():
                self._token('UNIQUE')
                with self._group():
                    self._token('VALUE')
            self._error('expecting one of: UNIQUE')

    @graken
    def _unique_specification_(self):
        with self._choice():
            with self._option():
                self._token('UNIQUE')
            with self._option():
                self._token('PRIMARY')
                self._token('KEY')
            self._error('expecting one of: PRIMARY UNIQUE')

    @graken
    def _referential_constraint_definition_(self):
        self._token('FOREIGN')
        self._token('KEY')
        self._token('(')
        self._column_name_list_()
        self._token(')')
        self._references_specification_()

    @graken
    def _references_specification_(self):
        self._token('REFERENCES')
        self._referenced_table_and_columns_()
        with self._optional():
            self._token('MATCH')
            self._match_type_()
        with self._optional():
            self._referential_triggered_action_()

    @graken
    def _match_type_(self):
        with self._choice():
            with self._option():
                self._token('FULL')
            with self._option():
                self._token('PARTIAL')
            with self._option():
                self._token('SIMPLE')
            self._error('expecting one of: FULL PARTIAL SIMPLE')

    @graken
    def _referenced_table_and_columns_(self):
        self._table_name_()
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')

    @graken
    def _referential_triggered_action_(self):
        with self._choice():
            with self._option():
                self._update_rule_()
                with self._optional():
                    self._delete_rule_()
            with self._option():
                self._delete_rule_()
                with self._optional():
                    self._update_rule_()
            self._error('no available options')

    @graken
    def _update_rule_(self):
        self._token('ON')
        self._token('UPDATE')
        self._referential_action_()

    @graken
    def _delete_rule_(self):
        self._token('ON')
        self._token('DELETE')
        self._referential_action_()

    @graken
    def _referential_action_(self):
        with self._choice():
            with self._option():
                self._token('CASCADE')
            with self._option():
                self._token('SET')
                self._token('NULL')
            with self._option():
                self._token('SET')
                self._token('DEFAULT')
            with self._option():
                self._token('RESTRICT')
            with self._option():
                self._token('NO')
                self._token('ACTION')
            self._error('expecting one of: CASCADE NO RESTRICT SET')

    @graken
    def _check_constraint_definition_(self):
        self._token('CHECK')
        self._token('(')
        self._search_condition_()
        self._token(')')

    @graken
    def _alter_table_statement_(self):
        self._token('ALTER')
        self._token('TABLE')
        self._table_name_()
        self._alter_table_action_()

    @graken
    def _alter_table_action_(self):
        with self._choice():
            with self._option():
                self._add_column_definition_()
            with self._option():
                self._alter_column_definition_()
            with self._option():
                self._drop_column_definition_()
            with self._option():
                self._add_table_constraint_definition_()
            with self._option():
                self._drop_table_constraint_definition_()
            self._error('no available options')

    @graken
    def _add_column_definition_(self):
        self._token('ADD')
        with self._optional():
            self._token('COLUMN')
        self._column_definition_()

    @graken
    def _alter_column_definition_(self):
        self._token('ALTER')
        with self._optional():
            self._token('COLUMN')
        self._column_name_()
        self._alter_column_action_()

    @graken
    def _alter_column_action_(self):
        with self._choice():
            with self._option():
                self._set_column_default_clause_()
            with self._option():
                self._drop_default_clause_()
            with self._option():
                self._add_column_scope_clause_()
            with self._option():
                self._drop_column_scope_clause_()
            with self._option():
                self._alter_identity_column_specification_()
            self._error('no available options')

    @graken
    def _set_column_default_clause_(self):
        self._token('SET')
        self._default_clause_()

    @graken
    def _drop_default_clause_(self):
        self._token('DROP')
        self._token('DEFAULT')

    @graken
    def _add_column_scope_clause_(self):
        self._token('ADD')
        self._scope_clause_()

    @graken
    def _drop_column_scope_clause_(self):
        self._token('DROP')
        self._token('SCOPE')
        self._drop_behavior_()

    @graken
    def _alter_identity_column_specification_(self):
        def block0():
            self._alter_identity_column_option_()

        self._positive_closure(block0)

    @graken
    def _alter_identity_column_option_(self):
        with self._choice():
            with self._option():
                self._alter_sequence_generator_restart_option_()
            with self._option():
                self._token('SET')
                self._basic_sequence_generator_option_()
            self._error('no available options')

    @graken
    def _drop_column_definition_(self):
        self._token('DROP')
        with self._optional():
            self._token('COLUMN')
        self._column_name_()
        self._drop_behavior_()

    @graken
    def _add_table_constraint_definition_(self):
        self._token('ADD')
        self._table_constraint_definition_()

    @graken
    def _drop_table_constraint_definition_(self):
        self._token('DROP')
        self._token('CONSTRAINT')
        self._constraint_name_()
        self._drop_behavior_()

    @graken
    def _drop_table_statement_(self):
        self._token('DROP')
        self._token('TABLE')
        self._table_name_()
        self._drop_behavior_()

    @graken
    def _view_definition_(self):
        self._token('CREATE')
        with self._optional():
            self._token('RECURSIVE')
        self._token('VIEW')
        self._table_name_()
        self._view_specification_()
        self._token('AS')
        self._query_expression_()
        with self._optional():
            self._token('WITH')
            with self._optional():
                self._levels_clause_()
            self._token('CHECK')
            self._token('OPTION')

    @graken
    def _view_specification_(self):
        with self._choice():
            with self._option():
                self._regular_view_specification_()
            with self._option():
                self._referenceable_view_specification_()
            self._error('no available options')

    @graken
    def _regular_view_specification_(self):
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')

    @graken
    def _referenceable_view_specification_(self):
        self._token('OF')
        self._path_resolved_user_defined_type_name_()
        with self._optional():
            self._subview_clause_()
        with self._optional():
            self._view_element_list_()

    @graken
    def _subview_clause_(self):
        self._token('UNDER')
        self._table_name_()

    @graken
    def _view_element_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._view_element_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _view_element_(self):
        with self._choice():
            with self._option():
                self._self_referencing_column_specification_()
            with self._option():
                self._view_column_option_()
            self._error('no available options')

    @graken
    def _view_column_option_(self):
        self._column_name_()
        self._token('WITH')
        self._token('OPTIONS')
        self._scope_clause_()

    @graken
    def _levels_clause_(self):
        with self._choice():
            with self._option():
                self._token('CASCADED')
            with self._option():
                self._token('LOCAL')
            self._error('expecting one of: CASCADED LOCAL')

    @graken
    def _drop_view_statement_(self):
        self._token('DROP')
        self._token('VIEW')
        self._table_name_()
        self._drop_behavior_()

    @graken
    def _domain_definition_(self):
        self._token('CREATE')
        self._token('DOMAIN')
        self._domain_name_()
        with self._optional():
            self._token('AS')
        self._data_type_()
        with self._optional():
            self._default_clause_()
        with self._optional():
            def block0():
                self._domain_constraint_()

            self._positive_closure(block0)
        with self._optional():
            self._collate_clause_()

    @graken
    def _domain_constraint_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._check_constraint_definition_()
        with self._optional():
            self._constraint_characteristics_()

    @graken
    def _alter_domain_statement_(self):
        self._token('ALTER')
        self._token('DOMAIN')
        self._domain_name_()
        self._alter_domain_action_()

    @graken
    def _alter_domain_action_(self):
        with self._choice():
            with self._option():
                self._set_domain_default_clause_()
            with self._option():
                self._drop_default_clause_()
            with self._option():
                self._add_domain_constraint_definition_()
            with self._option():
                self._drop_domain_constraint_definition_()
            self._error('no available options')

    @graken
    def _set_domain_default_clause_(self):
        self._token('SET')
        self._default_clause_()

    @graken
    def _add_domain_constraint_definition_(self):
        self._token('ADD')
        self._domain_constraint_()

    @graken
    def _drop_domain_constraint_definition_(self):
        self._token('DROP')
        self._token('CONSTRAINT')
        self._constraint_name_()

    @graken
    def _drop_domain_statement_(self):
        self._token('DROP')
        self._token('DOMAIN')
        self._domain_name_()
        self._drop_behavior_()

    @graken
    def _character_set_definition_(self):
        self._token('CREATE')
        self._token('CHARACTER')
        self._token('SET')
        self._character_set_name_()
        with self._optional():
            self._token('AS')
        self._character_set_source_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _character_set_source_(self):
        self._token('GET')
        self._character_set_name_()

    @graken
    def _drop_character_set_statement_(self):
        self._token('DROP')
        self._token('CHARACTER')
        self._token('SET')
        self._character_set_name_()

    @graken
    def _collation_definition_(self):
        self._token('CREATE')
        self._token('COLLATION')
        self._collation_name_()
        self._token('FOR')
        self._character_set_name_()
        self._token('FROM')
        self._collation_name_()
        with self._optional():
            self._pad_characteristic_()

    @graken
    def _pad_characteristic_(self):
        with self._choice():
            with self._option():
                self._token('NO')
                self._token('PAD')
            with self._option():
                self._token('PAD')
                self._token('SPACE')
            self._error('expecting one of: NO PAD')

    @graken
    def _drop_collation_statement_(self):
        self._token('DROP')
        self._token('COLLATION')
        self._collation_name_()
        self._drop_behavior_()

    @graken
    def _transliteration_definition_(self):
        self._token('CREATE')
        self._token('TRANSLATION')
        self._transliteration_name_()
        self._token('FOR')
        self._character_set_name_()
        self._token('TO')
        self._character_set_name_()
        self._token('FROM')
        self._transliteration_source_()

    @graken
    def _transliteration_source_(self):
        with self._choice():
            with self._option():
                self._transliteration_name_()
            with self._option():
                self._specific_routine_designator_()
            self._error('no available options')

    @graken
    def _drop_transliteration_statement_(self):
        self._token('DROP')
        self._token('TRANSLATION')
        self._transliteration_name_()

    @graken
    def _assertion_definition_(self):
        self._token('CREATE')
        self._token('ASSERTION')
        self._constraint_name_()
        self._token('CHECK')
        self._token('(')
        self._search_condition_()
        self._token(')')
        with self._optional():
            self._constraint_characteristics_()

    @graken
    def _drop_assertion_statement_(self):
        self._token('DROP')
        self._token('ASSERTION')
        self._constraint_name_()

    @graken
    def _trigger_definition_(self):
        self._token('CREATE')
        self._token('TRIGGER')
        self._trigger_name_()
        self._trigger_action_time_()
        self._trigger_event_()
        self._token('ON')
        self._table_name_()
        with self._optional():
            self._token('REFERENCING')

            def block0():
                self._old_or_new_values_alias_()

            self._positive_closure(block0)
        self._triggered_action_()

    @graken
    def _trigger_action_time_(self):
        with self._choice():
            with self._option():
                self._token('BEFORE')
            with self._option():
                self._token('AFTER')
            self._error('expecting one of: AFTER BEFORE')

    @graken
    def _trigger_event_(self):
        with self._choice():
            with self._option():
                self._token('INSERT')
            with self._option():
                self._token('DELETE')
            with self._option():
                self._token('UPDATE')
                with self._optional():
                    self._token('OF')
                    self._column_name_list_()
            self._error('expecting one of: DELETE INSERT UPDATE')

    @graken
    def _triggered_action_(self):
        with self._optional():
            self._token('FOR')
            self._token('EACH')
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('ROW')
                    with self._option():
                        self._token('STATEMENT')
                    self._error('expecting one of: ROW STATEMENT')
        with self._optional():
            self._token('WHEN')
            self._token('(')
            self._search_condition_()
            self._token(')')
        self._triggered_sql_statement_()

    @graken
    def _triggered_sql_statement_(self):
        with self._choice():
            with self._option():
                self._sql_procedure_statement_()
            with self._option():
                self._token('BEGIN')
                self._token('ATOMIC')

                def block0():
                    self._sql_procedure_statement_()
                    self._token(';')

                self._positive_closure(block0)
                self._token('END')
            self._error('no available options')

    @graken
    def _old_or_new_values_alias_(self):
        with self._choice():
            with self._option():
                self._token('OLD')
                with self._optional():
                    self._token('ROW')
                with self._optional():
                    self._token('AS')
                self._old_values_correlation_name_()
            with self._option():
                self._token('NEW')
                with self._optional():
                    self._token('ROW')
                with self._optional():
                    self._token('AS')
                self._new_values_correlation_name_()
            with self._option():
                self._token('OLD')
                self._token('TABLE')
                with self._optional():
                    self._token('AS')
                self._old_values_table_alias_()
            with self._option():
                self._token('NEW')
                self._token('TABLE')
                with self._optional():
                    self._token('AS')
                self._new_values_table_alias_()
            self._error('no available options')

    @graken
    def _old_values_table_alias_(self):
        self._identifier_()

    @graken
    def _new_values_table_alias_(self):
        self._identifier_()

    @graken
    def _old_values_correlation_name_(self):
        self._correlation_name_()

    @graken
    def _new_values_correlation_name_(self):
        self._correlation_name_()

    @graken
    def _drop_trigger_statement_(self):
        self._token('DROP')
        self._token('TRIGGER')
        self._trigger_name_()

    @graken
    def _user_defined_type_definition_(self):
        self._token('CREATE')
        self._token('TYPE')
        self._user_defined_type_body_()

    @graken
    def _user_defined_type_body_(self):
        self._schema_resolved_user_defined_type_name_()
        with self._optional():
            self._subtype_clause_()
        with self._optional():
            self._token('AS')
            self._representation_()
        with self._optional():
            self._user_defined_type_option_list_()
        with self._optional():
            self._method_specification_list_()

    @graken
    def _user_defined_type_option_list_(self):
        def block0():
            self._user_defined_type_option_()

        self._positive_closure(block0)

    @graken
    def _user_defined_type_option_(self):
        with self._choice():
            with self._option():
                self._instantiable_clause_()
            with self._option():
                self._finality_()
            with self._option():
                self._reference_type_specification_()
            with self._option():
                self._ref_cast_option_()
            with self._option():
                self._cast_option_()
            self._error('no available options')

    @graken
    def _subtype_clause_(self):
        self._token('UNDER')
        self._path_resolved_user_defined_type_name_()

    @graken
    def _representation_(self):
        with self._choice():
            with self._option():
                self._predefined_type_()
            with self._option():
                self._member_list_()
            self._error('no available options')

    @graken
    def _member_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._member_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _member_(self):
        self._attribute_definition_()

    @graken
    def _instantiable_clause_(self):
        with self._optional():
            self._token('NOT')
        self._token('INSTANTIABLE')

    @graken
    def _finality_(self):
        with self._optional():
            self._token('NOT')
        self._token('FINAL')

    @graken
    def _reference_type_specification_(self):
        with self._choice():
            with self._option():
                self._user_defined_representation_()
            with self._option():
                self._derived_representation_()
            with self._option():
                self._system_generated_representation_()
            self._error('no available options')

    @graken
    def _user_defined_representation_(self):
        self._token('REF')
        self._token('USING')
        self._predefined_type_()

    @graken
    def _derived_representation_(self):
        self._token('REF')
        self._token('FROM')
        self._list_of_attributes_()

    @graken
    def _system_generated_representation_(self):
        self._token('REF')
        self._token('IS')
        self._token('SYSTEM')
        self._token('GENERATED')

    @graken
    def _ref_cast_option_(self):
        with self._optional():
            self._cast_to_ref_()
        with self._optional():
            self._cast_to_type_()

    @graken
    def _cast_to_ref_(self):
        self._token('CAST')
        self._token('(')
        self._token('SOURCE')
        self._token('AS')
        self._token('REF')
        self._token(')')
        self._token('WITH')
        self._identifier_()

    @graken
    def _cast_to_type_(self):
        self._token('CAST')
        self._token('(')
        self._token('REF')
        self._token('AS')
        self._token('SOURCE')
        self._token(')')
        self._token('WITH')
        self._identifier_()

    @graken
    def _list_of_attributes_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._attribute_name_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _cast_option_(self):
        with self._optional():
            self._cast_to_distinct_()
        with self._optional():
            self._cast_to_source_()

    @graken
    def _cast_to_distinct_(self):
        self._token('CAST')
        self._token('(')
        self._token('SOURCE')
        self._token('AS')
        self._token('DISTINCT')
        self._token(')')
        self._token('WITH')
        self._identifier_()

    @graken
    def _cast_to_source_(self):
        self._token('CAST')
        self._token('(')
        self._token('DISTINCT')
        self._token('AS')
        self._token('SOURCE')
        self._token(')')
        self._token('WITH')
        self._identifier_()

    @graken
    def _method_specification_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._method_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _method_specification_(self):
        with self._choice():
            with self._option():
                self._original_method_specification_()
            with self._option():
                self._overriding_method_specification_()
            self._error('no available options')

    @graken
    def _original_method_specification_(self):
        self._partial_method_specification_()
        with self._optional():
            self._token('SELF')
            self._token('AS')
            self._token('RESULT')
        with self._optional():
            self._token('SELF')
            self._token('AS')
            self._token('LOCATOR')
        with self._optional():
            def block0():
                self._method_characteristic_()

            self._positive_closure(block0)

    @graken
    def _overriding_method_specification_(self):
        self._token('OVERRIDING')
        self._partial_method_specification_()

    @graken
    def _partial_method_specification_(self):
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('INSTANCE')
                with self._option():
                    self._token('STATIC')
                with self._option():
                    self._token('CONSTRUCTOR')
                self._error('expecting one of: CONSTRUCTOR INSTANCE STATIC')
        self._token('METHOD')
        self._method_name_()
        self._sql_parameter_declaration_list_()
        self._returns_clause_()
        with self._optional():
            self._token('SPECIFIC')
            self._specific_method_name_()

    @graken
    def _specific_method_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._qualified_identifier_()

    @graken
    def _method_characteristic_(self):
        with self._choice():
            with self._option():
                self._language_clause_()
            with self._option():
                self._parameter_style_clause_()
            with self._option():
                self._deterministic_characteristic_()
            with self._option():
                self._sql_data_access_indication_()
            with self._option():
                self._null_call_clause_()
            self._error('no available options')

    @graken
    def _attribute_definition_(self):
        self._attribute_name_()
        self._data_type_()
        with self._optional():
            self._reference_scope_check_()
        with self._optional():
            self._default_clause_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _alter_type_statement_(self):
        self._token('ALTER')
        self._token('TYPE')
        self._schema_resolved_user_defined_type_name_()
        self._alter_type_action_()

    @graken
    def _alter_type_action_(self):
        with self._choice():
            with self._option():
                self._add_attribute_definition_()
            with self._option():
                self._drop_attribute_definition_()
            with self._option():
                self._add_original_method_specification_()
            with self._option():
                self._add_overriding_method_specification_()
            with self._option():
                self._drop_method_specification_()
            self._error('no available options')

    @graken
    def _add_attribute_definition_(self):
        self._token('ADD')
        self._token('ATTRIBUTE')
        self._attribute_definition_()

    @graken
    def _drop_attribute_definition_(self):
        self._token('DROP')
        self._token('ATTRIBUTE')
        self._attribute_name_()
        self._token('RESTRICT')

    @graken
    def _add_original_method_specification_(self):
        self._token('ADD')
        self._original_method_specification_()

    @graken
    def _add_overriding_method_specification_(self):
        self._token('ADD')
        self._overriding_method_specification_()

    @graken
    def _drop_method_specification_(self):
        self._token('DROP')
        self._specific_method_specification_designator_()
        self._token('RESTRICT')

    @graken
    def _specific_method_specification_designator_(self):
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('INSTANCE')
                with self._option():
                    self._token('STATIC')
                with self._option():
                    self._token('CONSTRUCTOR')
                self._error('expecting one of: CONSTRUCTOR INSTANCE STATIC')
        self._token('METHOD')
        self._method_name_()
        self._data_type_list_()

    @graken
    def _drop_data_type_statement_(self):
        self._token('DROP')
        self._token('TYPE')
        self._schema_resolved_user_defined_type_name_()
        self._drop_behavior_()

    @graken
    def _schema_routine_(self):
        with self._choice():
            with self._option():
                self._schema_procedure_()
            with self._option():
                self._schema_function_()
            self._error('no available options')

    @graken
    def _schema_procedure_(self):
        self._token('CREATE')
        self._sql_invoked_procedure_()

    @graken
    def _schema_function_(self):
        self._token('CREATE')
        self._sql_invoked_function_()

    @graken
    def _sql_invoked_procedure_(self):
        self._token('PROCEDURE')
        self._schema_qualified_routine_name_()
        self._sql_parameter_declaration_list_()
        with self._optional():
            def block0():
                self._routine_characteristic_()

            self._positive_closure(block0)
        self._routine_body_()

    @graken
    def _sql_invoked_function_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._function_specification_()
                with self._option():
                    self._method_specification_designator_()
                self._error('no available options')
        self._routine_body_()

    @graken
    def _sql_parameter_declaration_list_(self):
        self._token('(')
        with self._optional():
            def sep0():
                self._token(',')

            def block0():
                self._sql_parameter_declaration_()

            self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _sql_parameter_declaration_(self):
        with self._optional():
            self._parameter_mode_()
        with self._optional():
            self._sql_parameter_name_()
        self._parameter_type_()
        with self._optional():
            self._token('RESULT')

    @graken
    def _parameter_mode_(self):
        with self._choice():
            with self._option():
                self._token('IN')
            with self._option():
                self._token('OUT')
            with self._option():
                self._token('INOUT')
            self._error('expecting one of: IN INOUT OUT')

    @graken
    def _parameter_type_(self):
        self._data_type_()
        with self._optional():
            self._token('AS')
            self._token('LOCATOR')

    @graken
    def _function_specification_(self):
        self._token('FUNCTION')
        self._schema_qualified_routine_name_()
        self._sql_parameter_declaration_list_()
        self._returns_clause_()
        with self._optional():
            def block0():
                self._routine_characteristic_()

            self._positive_closure(block0)
        with self._optional():
            self._token('STATIC')
            self._token('DISPATCH')

    @graken
    def _method_specification_designator_(self):
        with self._choice():
            with self._option():
                self._token('SPECIFIC')
                self._token('METHOD')
                self._specific_method_name_()
            with self._option():
                with self._optional():
                    with self._choice():
                        with self._option():
                            self._token('INSTANCE')
                        with self._option():
                            self._token('STATIC')
                        with self._option():
                            self._token('CONSTRUCTOR')
                        self._error('expecting one of: CONSTRUCTOR INSTANCE '
                                    'STATIC')
                self._token('METHOD')
                self._method_name_()
                self._sql_parameter_declaration_list_()
                with self._optional():
                    self._returns_clause_()
                self._token('FOR')
                self._schema_resolved_user_defined_type_name_()
            self._error('no available options')

    @graken
    def _routine_characteristic_(self):
        with self._choice():
            with self._option():
                self._language_clause_()
            with self._option():
                self._parameter_style_clause_()
            with self._option():
                self._token('SPECIFIC')
                self._specific_name_()
            with self._option():
                self._deterministic_characteristic_()
            with self._option():
                self._sql_data_access_indication_()
            with self._option():
                self._null_call_clause_()
            with self._option():
                self._dynamic_result_sets_characteristic_()
            with self._option():
                self._savepoint_level_indication_()
            self._error('no available options')

    @graken
    def _savepoint_level_indication_(self):
        with self._choice():
            with self._option():
                self._token('NEW')
                self._token('SAVEPOINT')
                self._token('LEVEL')
            with self._option():
                self._token('OLD')
                self._token('SAVEPOINT')
                self._token('LEVEL')
            self._error('expecting one of: NEW OLD')

    @graken
    def _dynamic_result_sets_characteristic_(self):
        self._token('DYNAMIC')
        self._token('RESULT')
        self._token('SETS')
        self._integer_()

    @graken
    def _parameter_style_clause_(self):
        self._token('PARAMETER')
        self._token('STYLE')
        self._parameter_style_()

    @graken
    def _returns_clause_(self):
        self._token('RETURNS')
        self._returns_type_()

    @graken
    def _returns_type_(self):
        with self._choice():
            with self._option():
                self._returns_data_type_()
                with self._optional():
                    self._result_cast_()
            with self._option():
                self._returns_table_type_()
            self._error('no available options')

    @graken
    def _returns_table_type_(self):
        self._token('TABLE')
        self._table_function_column_list_()

    @graken
    def _table_function_column_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._table_function_column_list_element_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _table_function_column_list_element_(self):
        self._column_name_()
        self._data_type_()

    @graken
    def _result_cast_(self):
        self._token('CAST')
        self._token('FROM')
        self._result_cast_from_type_()

    @graken
    def _result_cast_from_type_(self):
        self._data_type_()
        with self._optional():
            self._token('AS')
            self._token('LOCATOR')

    @graken
    def _returns_data_type_(self):
        self._data_type_()
        with self._optional():
            self._token('AS')
            self._token('LOCATOR')

    @graken
    def _routine_body_(self):
        with self._choice():
            with self._option():
                self._sql_routine_spec_()
            with self._option():
                self._external_body_reference_()
            self._error('no available options')

    @graken
    def _sql_routine_spec_(self):
        with self._optional():
            self._rights_clause_()
        self._sql_procedure_statement_()

    @graken
    def _rights_clause_(self):
        with self._choice():
            with self._option():
                self._token('SQL')
                self._token('SECURITY')
                self._token('INVOKER')
            with self._option():
                self._token('SQL')
                self._token('SECURITY')
                self._token('DEFINER')
            self._error('expecting one of: SQL')

    @graken
    def _external_body_reference_(self):
        self._token('EXTERNAL')
        with self._optional():
            self._token('NAME')
            self._external_routine_name_()
        with self._optional():
            self._parameter_style_clause_()
        with self._optional():
            self._transform_group_specification_()
        with self._optional():
            self._external_security_clause_()

    @graken
    def _external_security_clause_(self):
        with self._choice():
            with self._option():
                self._token('EXTERNAL')
                self._token('SECURITY')
                self._token('DEFINER')
            with self._option():
                self._token('EXTERNAL')
                self._token('SECURITY')
                self._token('INVOKER')
            with self._option():
                self._token('EXTERNAL')
                self._token('SECURITY')
                self._token('IMPLEMENTATION')
                self._token('DEFINED')
            self._error('expecting one of: EXTERNAL')

    @graken
    def _parameter_style_(self):
        with self._choice():
            with self._option():
                self._token('SQL')
            with self._option():
                self._token('GENERAL')
            self._error('expecting one of: GENERAL SQL')

    @graken
    def _deterministic_characteristic_(self):
        with self._optional():
            self._token('NOT')
        self._token('DETERMINISTIC')

    @graken
    def _sql_data_access_indication_(self):
        with self._choice():
            with self._option():
                self._token('NO')
                self._token('SQL')
            with self._option():
                self._token('CONTAINS')
                self._token('SQL')
            with self._option():
                self._token('READS')
                self._token('SQL')
                self._token('DATA')
            with self._option():
                self._token('MODIFIES')
                self._token('SQL')
                self._token('DATA')
            self._error('expecting one of: CONTAINS MODIFIES NO READS')

    @graken
    def _null_call_clause_(self):
        with self._choice():
            with self._option():
                self._token('RETURNS')
                self._token('NULL')
                self._token('ON')
                self._token('NULL')
                self._token('INPUT')
            with self._option():
                self._token('CALLED')
                self._token('ON')
                self._token('NULL')
                self._token('INPUT')
            self._error('expecting one of: CALLED RETURNS')

    @graken
    def _transform_group_specification_(self):
        self._token('TRANSFORM')
        self._token('GROUP')
        with self._group():
            with self._choice():
                with self._option():
                    self._group_name_()
                with self._option():
                    self._multiple_group_specification_()
                self._error('no available options')

    @graken
    def _multiple_group_specification_(self):
        def sep0():
            self._token(',')

        def block0():
            self._group_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _group_specification_(self):
        self._group_name_()
        self._token('FOR')
        self._token('TYPE')
        self._path_resolved_user_defined_type_name_()

    @graken
    def _alter_routine_statement_(self):
        self._token('ALTER')
        self._specific_routine_designator_()
        self._alter_routine_characteristics_()
        self._token('RESTRICT')

    @graken
    def _alter_routine_characteristics_(self):
        def block0():
            self._alter_routine_characteristic_()

        self._positive_closure(block0)

    @graken
    def _alter_routine_characteristic_(self):
        with self._choice():
            with self._option():
                self._language_clause_()
            with self._option():
                self._parameter_style_clause_()
            with self._option():
                self._sql_data_access_indication_()
            with self._option():
                self._null_call_clause_()
            with self._option():
                self._dynamic_result_sets_characteristic_()
            with self._option():
                self._token('NAME')
                self._external_routine_name_()
            self._error('no available options')

    @graken
    def _drop_routine_statement_(self):
        self._token('DROP')
        self._specific_routine_designator_()
        self._drop_behavior_()

    @graken
    def _user_defined_cast_definition_(self):
        self._token('CREATE')
        self._token('CAST')
        self._token('(')
        self._data_type_()
        self._token('AS')
        self._data_type_()
        self._token(')')
        self._token('WITH')
        self._cast_function_()
        with self._optional():
            self._token('AS')
            self._token('ASSIGNMENT')

    @graken
    def _cast_function_(self):
        self._specific_routine_designator_()

    @graken
    def _drop_user_defined_cast_statement_(self):
        self._token('DROP')
        self._token('CAST')
        self._token('(')
        self._data_type_()
        self._token('AS')
        self._data_type_()
        self._token(')')
        self._drop_behavior_()

    @graken
    def _user_defined_ordering_definition_(self):
        self._token('CREATE')
        self._token('ORDERING')
        self._token('FOR')
        self._schema_resolved_user_defined_type_name_()
        self._ordering_form_()

    @graken
    def _ordering_form_(self):
        with self._choice():
            with self._option():
                self._equals_ordering_form_()
            with self._option():
                self._full_ordering_form_()
            self._error('no available options')

    @graken
    def _equals_ordering_form_(self):
        self._token('EQUALS')
        self._token('ONLY')
        self._token('BY')
        self._ordering_category_()

    @graken
    def _full_ordering_form_(self):
        self._token('ORDER')
        self._token('FULL')
        self._token('BY')
        self._ordering_category_()

    @graken
    def _ordering_category_(self):
        with self._choice():
            with self._option():
                self._relative_category_()
            with self._option():
                self._map_category_()
            with self._option():
                self._state_category_()
            self._error('no available options')

    @graken
    def _relative_category_(self):
        self._token('RELATIVE')
        self._token('WITH')
        self._specific_routine_designator_()

    @graken
    def _map_category_(self):
        self._token('MAP')
        self._token('WITH')
        self._specific_routine_designator_()

    @graken
    def _state_category_(self):
        self._token('STATE')
        with self._optional():
            self._specific_name_()

    @graken
    def _drop_user_defined_ordering_statement_(self):
        self._token('DROP')
        self._token('ORDERING')
        self._token('FOR')
        self._schema_resolved_user_defined_type_name_()
        self._drop_behavior_()

    @graken
    def _transform_definition_(self):
        self._token('CREATE')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('TRANSFORM')
                with self._option():
                    self._token('TRANSFORMS')
                self._error('expecting one of: TRANSFORM TRANSFORMS')
        self._token('FOR')
        self._schema_resolved_user_defined_type_name_()

        def block1():
            self._transform_group_()

        self._positive_closure(block1)

    @graken
    def _transform_group_(self):
        self._group_name_()
        self._token('(')
        self._transform_element_list_()
        self._token(')')

    @graken
    def _group_name_(self):
        self._identifier_()

    @graken
    def _transform_element_list_(self):
        self._transform_element_()
        with self._optional():
            self._token(',')
            self._transform_element_()

    @graken
    def _transform_element_(self):
        self._transform_kind_()
        self._token('WITH')
        self._specific_routine_designator_()

    @graken
    def _alter_transform_statement_(self):
        self._token('ALTER')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('TRANSFORM')
                with self._option():
                    self._token('TRANSFORMS')
                self._error('expecting one of: TRANSFORM TRANSFORMS')
        self._token('FOR')
        self._schema_resolved_user_defined_type_name_()

        def block1():
            self._alter_group_()

        self._positive_closure(block1)

    @graken
    def _alter_group_(self):
        self._group_name_()
        self._token('(')
        self._alter_transform_action_list_()
        self._token(')')

    @graken
    def _alter_transform_action_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._alter_transform_action_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _alter_transform_action_(self):
        with self._choice():
            with self._option():
                self._add_transform_element_list_()
            with self._option():
                self._drop_transform_element_list_()
            self._error('no available options')

    @graken
    def _add_transform_element_list_(self):
        self._token('ADD')
        self._token('(')
        self._transform_element_list_()
        self._token(')')

    @graken
    def _drop_transform_element_list_(self):
        self._token('DROP')
        self._token('(')
        self._transform_kind_()
        with self._optional():
            self._token(',')
            self._transform_kind_()
        self._drop_behavior_()
        self._token(')')

    @graken
    def _transform_kind_(self):
        with self._choice():
            with self._option():
                self._token('TO')
                self._token('SQL')
            with self._option():
                self._token('FROM')
                self._token('SQL')
            self._error('expecting one of: FROM TO')

    @graken
    def _drop_transform_statement_(self):
        self._token('DROP')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('TRANSFORM')
                with self._option():
                    self._token('TRANSFORMS')
                self._error('expecting one of: TRANSFORM TRANSFORMS')
        self._transforms_to_be_dropped_()
        self._token('FOR')
        self._schema_resolved_user_defined_type_name_()
        self._drop_behavior_()

    @graken
    def _transforms_to_be_dropped_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
            with self._option():
                self._group_name_()
            self._error('expecting one of: ALL')

    @graken
    def _sequence_generator_definition_(self):
        self._token('CREATE')
        self._token('SEQUENCE')
        self._sequence_generator_name_()
        with self._optional():
            self._sequence_generator_options_()

    @graken
    def _sequence_generator_options_(self):
        def block0():
            self._sequence_generator_option_()

        self._positive_closure(block0)

    @graken
    def _sequence_generator_option_(self):
        with self._choice():
            with self._option():
                self._sequence_generator_data_type_option_()
            with self._option():
                self._common_sequence_generator_options_()
            self._error('no available options')

    @graken
    def _common_sequence_generator_options_(self):
        def block0():
            self._common_sequence_generator_option_()

        self._positive_closure(block0)

    @graken
    def _common_sequence_generator_option_(self):
        with self._choice():
            with self._option():
                self._sequence_generator_start_with_option_()
            with self._option():
                self._basic_sequence_generator_option_()
            self._error('no available options')

    @graken
    def _basic_sequence_generator_option_(self):
        with self._choice():
            with self._option():
                self._sequence_generator_increment_by_option_()
            with self._option():
                self._sequence_generator_maxvalue_option_()
            with self._option():
                self._sequence_generator_minvalue_option_()
            with self._option():
                self._sequence_generator_cycle_option_()
            self._error('no available options')

    @graken
    def _sequence_generator_data_type_option_(self):
        self._token('AS')
        self._data_type_()

    @graken
    def _sequence_generator_start_with_option_(self):
        self._token('START')
        self._token('WITH')
        self._signed_numeric_literal_()

    @graken
    def _sequence_generator_increment_by_option_(self):
        self._token('INCREMENT')
        self._token('BY')
        self._signed_numeric_literal_()

    @graken
    def _sequence_generator_maxvalue_option_(self):
        with self._choice():
            with self._option():
                self._token('MAXVALUE')
                self._signed_numeric_literal_()
            with self._option():
                self._token('NO')
                self._token('MAXVALUE')
            self._error('expecting one of: NO')

    @graken
    def _sequence_generator_minvalue_option_(self):
        with self._choice():
            with self._option():
                self._token('MINVALUE')
                self._signed_numeric_literal_()
            with self._option():
                self._token('NO')
                self._token('MINVALUE')
            self._error('expecting one of: NO')

    @graken
    def _sequence_generator_cycle_option_(self):
        with self._optional():
            self._token('NO')
        self._token('CYCLE')

    @graken
    def _alter_sequence_generator_statement_(self):
        self._token('ALTER')
        self._token('SEQUENCE')
        self._sequence_generator_name_()
        self._alter_sequence_generator_options_()

    @graken
    def _alter_sequence_generator_options_(self):
        def block0():
            self._alter_sequence_generator_option_()

        self._positive_closure(block0)

    @graken
    def _alter_sequence_generator_option_(self):
        with self._choice():
            with self._option():
                self._alter_sequence_generator_restart_option_()
            with self._option():
                self._basic_sequence_generator_option_()
            self._error('no available options')

    @graken
    def _alter_sequence_generator_restart_option_(self):
        self._token('RESTART')
        self._token('WITH')
        self._signed_numeric_literal_()

    @graken
    def _drop_sequence_generator_statement_(self):
        self._token('DROP')
        self._token('SEQUENCE')
        self._sequence_generator_name_()
        self._drop_behavior_()

    @graken
    def _grant_statement_(self):
        with self._choice():
            with self._option():
                self._grant_privilege_statement_()
            with self._option():
                self._grant_role_statement_()
            self._error('no available options')

    @graken
    def _grant_privilege_statement_(self):
        self._token('GRANT')
        self._privileges_()
        self._token('TO')

        def sep0():
            self._token(',')

        def block0():
            self._grantee_()

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token('WITH')
            self._token('HIERARCHY')
            self._token('OPTION')
        with self._optional():
            self._token('WITH')
            self._token('GRANT')
            self._token('OPTION')
        with self._optional():
            self._token('GRANTED')
            self._token('BY')
            self._grantor_()

    @graken
    def _privileges_(self):
        self._object_privileges_()
        self._token('ON')
        self._object_name_()

    @graken
    def _object_name_(self):
        with self._choice():
            with self._option():
                with self._optional():
                    self._token('TABLE')
                self._table_name_()
            with self._option():
                self._token('DOMAIN')
                self._domain_name_()
            with self._option():
                self._token('COLLATION')
                self._collation_name_()
            with self._option():
                self._token('CHARACTER')
                self._token('SET')
                self._character_set_name_()
            with self._option():
                self._token('TRANSLATION')
                self._transliteration_name_()
            with self._option():
                self._token('TYPE')
                self._schema_resolved_user_defined_type_name_()
            with self._option():
                self._token('SEQUENCE')
                self._sequence_generator_name_()
            with self._option():
                self._specific_routine_designator_()
            self._error('no available options')

    @graken
    def _object_privileges_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
                self._token('PRIVILEGES')
            with self._option():
                def sep0():
                    self._token(',')

                def block0():
                    self._action_()

                self._positive_closure(block0, prefix=sep0)
            self._error('expecting one of: ALL')

    @graken
    def _action_(self):
        with self._choice():
            with self._option():
                self._token('SELECT')
            with self._option():
                self._token('SELECT')
                self._token('(')
                self._column_name_list_()
                self._token(')')
            with self._option():
                self._token('SELECT')
                self._token('(')
                self._privilege_method_list_()
                self._token(')')
            with self._option():
                self._token('DELETE')
            with self._option():
                self._token('INSERT')
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._token('UPDATE')
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._token('REFERENCES')
                with self._optional():
                    self._token('(')
                    self._column_name_list_()
                    self._token(')')
            with self._option():
                self._token('USAGE')
            with self._option():
                self._token('TRIGGER')
            with self._option():
                self._token('UNDER')
            with self._option():
                self._token('EXECUTE')
            self._error('expecting one of: DELETE EXECUTE INSERT REFERENCES '
                        'SELECT TRIGGER UNDER UPDATE USAGE')

    @graken
    def _privilege_method_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._specific_routine_designator_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _grantee_(self):
        with self._choice():
            with self._option():
                self._token('PUBLIC')
            with self._option():
                self._authorization_identifier_()
            self._error('expecting one of: PUBLIC')

    @graken
    def _grantor_(self):
        with self._choice():
            with self._option():
                self._token('CURRENT_USER')
            with self._option():
                self._token('CURRENT_ROLE')
            self._error('expecting one of: CURRENT_ROLE CURRENT_USER')

    @graken
    def _role_definition_(self):
        self._token('CREATE')
        self._token('ROLE')
        self._role_name_()
        with self._optional():
            self._token('WITH')
            self._token('ADMIN')
            self._grantor_()

    @graken
    def _grant_role_statement_(self):
        self._token('GRANT')

        def sep0():
            self._token(',')

        def block0():
            self._role_name_()

        self._positive_closure(block0, prefix=sep0)
        self._token('TO')

        def sep1():
            self._token(',')

        def block1():
            self._grantee_()

        self._positive_closure(block1, prefix=sep1)
        with self._optional():
            self._token('WITH')
            self._token('ADMIN')
            self._token('OPTION')
        with self._optional():
            self._token('GRANTED')
            self._token('BY')
            self._grantor_()

    @graken
    def _drop_role_statement_(self):
        self._token('DROP')
        self._token('ROLE')
        self._role_name_()

    @graken
    def _revoke_statement_(self):
        with self._choice():
            with self._option():
                self._revoke_privilege_statement_()
            with self._option():
                self._revoke_role_statement_()
            self._error('no available options')

    @graken
    def _revoke_privilege_statement_(self):
        self._token('REVOKE')
        with self._optional():
            self._revoke_option_extension_()
        self._privileges_()
        self._token('FROM')

        def sep0():
            self._token(',')

        def block0():
            self._grantee_()

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token('GRANTED')
            self._token('BY')
            self._grantor_()
        self._drop_behavior_()

    @graken
    def _revoke_option_extension_(self):
        with self._choice():
            with self._option():
                self._token('GRANT')
                self._token('OPTION')
                self._token('FOR')
            with self._option():
                self._token('HIERARCHY')
                self._token('OPTION')
                self._token('FOR')
            self._error('expecting one of: GRANT HIERARCHY')

    @graken
    def _revoke_role_statement_(self):
        self._token('REVOKE')
        with self._optional():
            self._token('ADMIN')
            self._token('OPTION')
            self._token('FOR')

        def sep0():
            self._token(',')

        def block0():
            self._role_name_()

        self._positive_closure(block0, prefix=sep0)
        self._token('FROM')

        def sep1():
            self._token(',')

        def block1():
            self._grantee_()

        self._positive_closure(block1, prefix=sep1)
        with self._optional():
            self._token('GRANTED')
            self._token('BY')
            self._grantor_()
        self._drop_behavior_()

    @graken
    def _character_set_specification_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._character_set_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _sql_procedure_statement_(self):
        self._sql_executable_statement_()

    @graken
    def _sql_executable_statement_(self):
        with self._choice():
            with self._option():
                self._sql_schema_statement_()
            with self._option():
                self._sql_data_statement_()
            with self._option():
                self._sql_control_statement_()
            with self._option():
                self._sql_transaction_statement_()
            with self._option():
                self._sql_connection_statement_()
            with self._option():
                self._sql_session_statement_()
            with self._option():
                self._sql_diagnostics_statement_()
            with self._option():
                self._sql_dynamic_statement_()
            self._error('no available options')

    @graken
    def _sql_schema_statement_(self):
        with self._choice():
            with self._option():
                self._sql_schema_definition_statement_()
            with self._option():
                self._sql_schema_manipulation_statement_()
            self._error('no available options')

    @graken
    def _sql_schema_definition_statement_(self):
        with self._choice():
            with self._option():
                self._schema_definition_()
            with self._option():
                self._table_definition_()
            with self._option():
                self._view_definition_()
            with self._option():
                self._schema_routine_()
            with self._option():
                self._grant_statement_()
            with self._option():
                self._role_definition_()
            with self._option():
                self._domain_definition_()
            with self._option():
                self._character_set_definition_()
            with self._option():
                self._collation_definition_()
            with self._option():
                self._transliteration_definition_()
            with self._option():
                self._assertion_definition_()
            with self._option():
                self._trigger_definition_()
            with self._option():
                self._user_defined_type_definition_()
            with self._option():
                self._user_defined_cast_definition_()
            with self._option():
                self._user_defined_ordering_definition_()
            with self._option():
                self._transform_definition_()
            with self._option():
                self._sequence_generator_definition_()
            self._error('no available options')

    @graken
    def _sql_schema_manipulation_statement_(self):
        with self._choice():
            with self._option():
                self._drop_schema_statement_()
            with self._option():
                self._alter_table_statement_()
            with self._option():
                self._drop_table_statement_()
            with self._option():
                self._drop_view_statement_()
            with self._option():
                self._alter_routine_statement_()
            with self._option():
                self._drop_routine_statement_()
            with self._option():
                self._drop_user_defined_cast_statement_()
            with self._option():
                self._revoke_statement_()
            with self._option():
                self._drop_role_statement_()
            with self._option():
                self._alter_domain_statement_()
            with self._option():
                self._drop_domain_statement_()
            with self._option():
                self._drop_character_set_statement_()
            with self._option():
                self._drop_collation_statement_()
            with self._option():
                self._drop_transliteration_statement_()
            with self._option():
                self._drop_assertion_statement_()
            with self._option():
                self._drop_trigger_statement_()
            with self._option():
                self._alter_type_statement_()
            with self._option():
                self._drop_data_type_statement_()
            with self._option():
                self._drop_user_defined_ordering_statement_()
            with self._option():
                self._alter_transform_statement_()
            with self._option():
                self._drop_transform_statement_()
            with self._option():
                self._alter_sequence_generator_statement_()
            with self._option():
                self._drop_sequence_generator_statement_()
            self._error('no available options')

    @graken
    def _sql_data_statement_(self):
        with self._choice():
            with self._option():
                self._open_statement_()
            with self._option():
                self._fetch_statement_()
            with self._option():
                self._close_statement_()
            with self._option():
                self._select_statement_single_row_()
            with self._option():
                self._free_locator_statement_()
            with self._option():
                self._hold_locator_statement_()
            with self._option():
                self._sql_data_change_statement_()
            self._error('no available options')

    @graken
    def _sql_data_change_statement_(self):
        with self._choice():
            with self._option():
                self._delete_statement_positioned_()
            with self._option():
                self._delete_statement_searched_()
            with self._option():
                self._insert_statement_()
            with self._option():
                self._update_statement_positioned_()
            with self._option():
                self._update_statement_searched_()
            with self._option():
                self._merge_statement_()
            self._error('no available options')

    @graken
    def _sql_control_statement_(self):
        with self._choice():
            with self._option():
                self._call_statement_()
            with self._option():
                self._return_statement_()
            self._error('no available options')

    @graken
    def _sql_transaction_statement_(self):
        with self._choice():
            with self._option():
                self._start_transaction_statement_()
            with self._option():
                self._set_transaction_statement_()
            with self._option():
                self._set_constraints_mode_statement_()
            with self._option():
                self._savepoint_statement_()
            with self._option():
                self._release_savepoint_statement_()
            with self._option():
                self._commit_statement_()
            with self._option():
                self._rollback_statement_()
            self._error('no available options')

    @graken
    def _sql_connection_statement_(self):
        with self._choice():
            with self._option():
                self._connect_statement_()
            with self._option():
                self._set_connection_statement_()
            with self._option():
                self._disconnect_statement_()
            self._error('no available options')

    @graken
    def _sql_session_statement_(self):
        with self._choice():
            with self._option():
                self._set_session_user_identifier_statement_()
            with self._option():
                self._set_role_statement_()
            with self._option():
                self._set_local_time_zone_statement_()
            with self._option():
                self._set_session_characteristics_statement_()
            with self._option():
                self._set_catalog_statement_()
            with self._option():
                self._set_schema_statement_()
            with self._option():
                self._set_names_statement_()
            with self._option():
                self._set_path_statement_()
            with self._option():
                self._set_transform_group_statement_()
            with self._option():
                self._set_session_collation_statement_()
            self._error('no available options')

    @graken
    def _sql_dynamic_statement_(self):
        with self._choice():
            with self._option():
                self._system_descriptor_statement_()
            with self._option():
                self._prepare_statement_()
            with self._option():
                self._deallocate_prepared_statement_()
            with self._option():
                self._describe_statement_()
            with self._option():
                self._execute_statement_()
            with self._option():
                self._execute_immediate_statement_()
            with self._option():
                self._sql_dynamic_data_statement_()
            self._error('no available options')

    @graken
    def _sql_dynamic_data_statement_(self):
        with self._choice():
            with self._option():
                self._allocate_cursor_statement_()
            with self._option():
                self._dynamic_open_statement_()
            with self._option():
                self._dynamic_fetch_statement_()
            with self._option():
                self._dynamic_close_statement_()
            with self._option():
                self._dynamic_delete_statement_positioned_()
            with self._option():
                self._dynamic_update_statement_positioned_()
            self._error('no available options')

    @graken
    def _system_descriptor_statement_(self):
        with self._choice():
            with self._option():
                self._allocate_descriptor_statement_()
            with self._option():
                self._deallocate_descriptor_statement_()
            with self._option():
                self._set_descriptor_statement_()
            with self._option():
                self._get_descriptor_statement_()
            self._error('no available options')

    @graken
    def _cursor_sensitivity_(self):
        with self._choice():
            with self._option():
                self._token('SENSITIVE')
            with self._option():
                self._token('INSENSITIVE')
            with self._option():
                self._token('ASENSITIVE')
            self._error('expecting one of: ASENSITIVE INSENSITIVE SENSITIVE')

    @graken
    def _cursor_scrollability_(self):
        with self._optional():
            self._token('NO')
        self._token('SCROLL')

    @graken
    def _cursor_holdability_(self):
        with self._choice():
            with self._option():
                self._token('WITH')
                self._token('HOLD')
            with self._option():
                self._token('WITHOUT')
                self._token('HOLD')
            self._error('expecting one of: WITH WITHOUT')

    @graken
    def _cursor_returnability_(self):
        with self._choice():
            with self._option():
                self._token('WITH')
                self._token('RETURN')
            with self._option():
                self._token('WITHOUT')
                self._token('RETURN')
            self._error('expecting one of: WITH WITHOUT')

    @graken
    def _updatability_clause_(self):
        self._token('FOR')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('READ')
                    self._token('ONLY')
                with self._option():
                    self._token('UPDATE')
                    with self._optional():
                        self._token('OF')
                        self._column_name_list_()
                self._error('expecting one of: READ UPDATE')

    @graken
    def _order_by_clause_(self):
        self._token('ORDER')
        self._token('BY')
        self._sort_specification_list_()

    @graken
    def _open_statement_(self):
        self._token('OPEN')
        self._cursor_name_()

    @graken
    def _fetch_statement_(self):
        self._token('FETCH')
        with self._optional():
            with self._optional():
                self._fetch_orientation_()
            self._token('FROM')
        self._cursor_name_()
        self._token('INTO')
        self._fetch_target_list_()

    @graken
    def _fetch_orientation_(self):
        with self._choice():
            with self._option():
                self._token('NEXT')
            with self._option():
                self._token('PRIOR')
            with self._option():
                self._token('FIRST')
            with self._option():
                self._token('LAST')
            with self._option():
                with self._group():
                    with self._choice():
                        with self._option():
                            self._token('ABSOLUTE')
                        with self._option():
                            self._token('RELATIVE')
                        self._error('expecting one of: ABSOLUTE RELATIVE')
                self._simple_value_specification_()
            self._error('expecting one of: FIRST LAST NEXT PRIOR')

    @graken
    def _fetch_target_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._target_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _close_statement_(self):
        self._token('CLOSE')
        self._cursor_name_()

    @graken
    def _select_statement_single_row_(self):
        self._token('SELECT')
        with self._optional():
            self._set_quantifier_()
        self._select_list_()
        self._token('INTO')
        self._select_target_list_()
        self._table_expression_()

    @graken
    def _select_target_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._target_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _delete_statement_positioned_(self):
        self._token('DELETE')
        self._token('FROM')
        self._target_table_()
        self._token('WHERE')
        self._token('CURRENT')
        self._token('OF')
        self._cursor_name_()

    @graken
    def _target_table_(self):
        with self._choice():
            with self._option():
                self._table_name_()
            with self._option():
                self._token('ONLY')
                self._token('(')
                self._table_name_()
                self._token(')')
            self._error('no available options')

    @graken
    def _delete_statement_searched_(self):
        self._token('DELETE')
        self._token('FROM')
        self._target_table_()
        with self._optional():
            self._token('WHERE')
            self._search_condition_()

    @graken
    def _insert_statement_(self):
        self._token('INSERT')
        self._token('INTO')
        self._table_name_()
        self._insert_columns_and_source_()

    @graken
    def _insert_columns_and_source_(self):
        with self._choice():
            with self._option():
                self._from_subquery_()
            with self._option():
                self._from_constructor_()
            with self._option():
                self._token('DEFAULT')
                self._token('VALUES')
            self._error('expecting one of: DEFAULT')

    @graken
    def _from_subquery_(self):
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')
        with self._optional():
            self._override_clause_()
        self._query_expression_()

    @graken
    def _from_constructor_(self):
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')
        with self._optional():
            self._override_clause_()
        self._contextually_typed_table_value_constructor_()

    @graken
    def _override_clause_(self):
        with self._choice():
            with self._option():
                self._token('OVERRIDING')
                self._token('USER')
                self._token('VALUE')
            with self._option():
                self._token('OVERRIDING')
                self._token('SYSTEM')
                self._token('VALUE')
            self._error('expecting one of: OVERRIDING')

    @graken
    def _merge_statement_(self):
        self._token('MERGE')
        self._token('INTO')
        self._target_table_()
        with self._optional():
            with self._optional():
                self._token('AS')
            self._correlation_name_()
        self._token('USING')
        self._table_reference_()
        self._token('ON')
        self._search_condition_()
        self._merge_operation_specification_()

    @graken
    def _merge_operation_specification_(self):
        def block0():
            self._merge_when_clause_()

        self._positive_closure(block0)

    @graken
    def _merge_when_clause_(self):
        with self._choice():
            with self._option():
                self._merge_when_matched_clause_()
            with self._option():
                self._merge_when_not_matched_clause_()
            self._error('no available options')

    @graken
    def _merge_when_matched_clause_(self):
        self._token('WHEN')
        self._token('MATCHED')
        self._token('THEN')
        self._merge_update_specification_()

    @graken
    def _merge_when_not_matched_clause_(self):
        self._token('WHEN')
        self._token('NOT')
        self._token('MATCHED')
        self._token('THEN')
        self._merge_insert_specification_()

    @graken
    def _merge_update_specification_(self):
        self._token('UPDATE')
        self._token('SET')
        self._set_clause_list_()

    @graken
    def _merge_insert_specification_(self):
        self._token('INSERT')
        with self._optional():
            self._token('(')
            self._column_name_list_()
            self._token(')')
        with self._optional():
            self._override_clause_()
        self._token('VALUES')
        self._merge_insert_value_list_()

    @graken
    def _merge_insert_value_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._merge_insert_value_element_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _merge_insert_value_element_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._contextually_typed_value_specification_()
            self._error('no available options')

    @graken
    def _update_statement_positioned_(self):
        self._token('UPDATE')
        self._target_table_()
        self._token('SET')
        self._set_clause_list_()
        self._token('WHERE')
        self._token('CURRENT')
        self._token('OF')
        self._cursor_name_()

    @graken
    def _update_statement_searched_(self):
        self._token('UPDATE')
        self._target_table_()
        self._token('SET')
        self._set_clause_list_()
        with self._optional():
            self._token('WHERE')
            self._search_condition_()

    @graken
    def _set_clause_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._set_clause_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _set_clause_(self):
        with self._choice():
            with self._option():
                self._multiple_column_assignment_()
            with self._option():
                self._set_target_()
                self._token('=')
                self._update_source_()
            self._error('no available options')

    @graken
    def _set_target_(self):
        with self._choice():
            with self._option():
                self._update_target_()
            with self._option():
                self._mutated_set_clause_()
            self._error('no available options')

    @graken
    def _multiple_column_assignment_(self):
        self._set_target_list_()
        self._token('=')
        self._contextually_typed_row_value_expression_()

    @graken
    def _set_target_list_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._set_target_()

        self._positive_closure(block0, prefix=sep0)
        self._token(')')

    @graken
    def _update_target_(self):
        self._column_name_()
        with self._optional():
            self._left_bracket_or_trigraph_()
            self._simple_value_specification_()
            self._right_bracket_or_trigraph_()

    @graken
    def _mutated_set_clause_(self):
        self._mutated_target_()
        self._token('.')
        self._method_name_()

    @graken
    def _mutated_target_(self):
        with self._choice():
            with self._option():
                self._column_name_()
            with self._option():
                self._mutated_set_clause_()
            self._error('no available options')

    @graken
    def _update_source_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._contextually_typed_value_specification_()
            self._error('no available options')

    @graken
    def _temporary_table_declaration_(self):
        self._token('DECLARE')
        self._token('LOCAL')
        self._token('TEMPORARY')
        self._token('TABLE')
        self._table_name_()
        self._table_element_list_()
        with self._optional():
            self._token('ON')
            self._token('COMMIT')
            self._table_commit_action_()
            self._token('ROWS')

    @graken
    def _free_locator_statement_(self):
        self._token('FREE')
        self._token('LOCATOR')

        def sep0():
            self._token(',')

        def block0():
            self._host_parameter_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _hold_locator_statement_(self):
        self._token('HOLD')
        self._token('LOCATOR')

        def sep0():
            self._token(',')

        def block0():
            self._host_parameter_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _call_statement_(self):
        self._token('CALL')
        self._routine_invocation_()

    @graken
    def _return_statement_(self):
        self._token('RETURN')
        self._return_value_()

    @graken
    def _return_value_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._token('NULL')
            self._error('expecting one of: NULL')

    @graken
    def _start_transaction_statement_(self):
        self._token('START')
        self._token('TRANSACTION')
        with self._optional():
            def sep0():
                self._token(',')

            def block0():
                self._transaction_mode_()

            self._positive_closure(block0, prefix=sep0)

    @graken
    def _transaction_mode_(self):
        with self._choice():
            with self._option():
                self._isolation_level_()
            with self._option():
                self._transaction_access_mode_()
            with self._option():
                self._diagnostics_size_()
            self._error('no available options')

    @graken
    def _transaction_access_mode_(self):
        with self._choice():
            with self._option():
                self._token('READ')
                self._token('ONLY')
            with self._option():
                self._token('READ')
                self._token('WRITE')
            self._error('expecting one of: READ')

    @graken
    def _isolation_level_(self):
        self._token('ISOLATION')
        self._token('LEVEL')
        self._level_of_isolation_()

    @graken
    def _level_of_isolation_(self):
        with self._choice():
            with self._option():
                self._token('READ')
                self._token('UNCOMMITTED')
            with self._option():
                self._token('READ')
                self._token('COMMITTED')
            with self._option():
                self._token('REPEATABLE')
                self._token('READ')
            with self._option():
                self._token('SERIALIZABLE')
            self._error('expecting one of: READ REPEATABLE SERIALIZABLE')

    @graken
    def _diagnostics_size_(self):
        self._token('DIAGNOSTICS')
        self._token('SIZE')
        self._number_of_conditions_()

    @graken
    def _number_of_conditions_(self):
        self._simple_value_specification_()

    @graken
    def _set_transaction_statement_(self):
        self._token('SET')
        with self._optional():
            self._token('LOCAL')
        self._transaction_characteristics_()

    @graken
    def _transaction_characteristics_(self):
        self._token('TRANSACTION')

        def sep0():
            self._token(',')

        def block0():
            self._transaction_mode_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _set_constraints_mode_statement_(self):
        self._token('SET')
        self._token('CONSTRAINTS')
        self._constraint_name_list_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('DEFERRED')
                with self._option():
                    self._token('IMMEDIATE')
                self._error('expecting one of: DEFERRED IMMEDIATE')

    @graken
    def _constraint_name_list_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
            with self._option():
                def sep0():
                    self._token(',')

                def block0():
                    self._constraint_name_()

                self._positive_closure(block0, prefix=sep0)
            self._error('expecting one of: ALL')

    @graken
    def _savepoint_statement_(self):
        self._token('SAVEPOINT')
        self._savepoint_name_()

    @graken
    def _release_savepoint_statement_(self):
        self._token('RELEASE')
        self._token('SAVEPOINT')
        self._savepoint_name_()

    @graken
    def _commit_statement_(self):
        self._token('COMMIT')
        with self._optional():
            self._token('WORK')
        with self._optional():
            self._token('AND')
            with self._optional():
                self._token('NO')
            self._token('CHAIN')

    @graken
    def _rollback_statement_(self):
        self._token('ROLLBACK')
        with self._optional():
            self._token('WORK')
        with self._optional():
            self._token('AND')
            with self._optional():
                self._token('NO')
            self._token('CHAIN')
        with self._optional():
            self._savepoint_clause_()

    @graken
    def _savepoint_clause_(self):
        self._token('TO')
        self._token('SAVEPOINT')
        self._savepoint_name_()

    @graken
    def _connect_statement_(self):
        self._token('CONNECT')
        self._token('TO')
        self._connection_target_()

    @graken
    def _connection_target_(self):
        with self._choice():
            with self._option():
                self._sql_server_name_()
                with self._optional():
                    self._token('AS')
                    self._connection_name_()
                with self._optional():
                    self._token('USER')
                    self._connection_user_name_()
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT')

    @graken
    def _set_connection_statement_(self):
        self._token('SET')
        self._token('CONNECTION')
        self._connection_object_()

    @graken
    def _connection_object_(self):
        with self._choice():
            with self._option():
                self._token('DEFAULT')
            with self._option():
                self._connection_name_()
            self._error('expecting one of: DEFAULT')

    @graken
    def _disconnect_statement_(self):
        self._token('DISCONNECT')
        self._disconnect_object_()

    @graken
    def _disconnect_object_(self):
        with self._choice():
            with self._option():
                self._connection_object_()
            with self._option():
                self._token('ALL')
            with self._option():
                self._token('CURRENT')
            self._error('expecting one of: ALL CURRENT')

    @graken
    def _set_session_characteristics_statement_(self):
        self._token('SET')
        self._token('SESSION')
        self._token('CHARACTERISTICS')
        self._token('AS')
        self._session_characteristic_list_()

    @graken
    def _session_characteristic_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._transaction_characteristics_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _set_session_user_identifier_statement_(self):
        self._token('SET')
        self._token('SESSION')
        self._token('AUTHORIZATION')
        self._value_specification_()

    @graken
    def _set_role_statement_(self):
        self._token('SET')
        self._token('ROLE')
        self._role_specification_()

    @graken
    def _role_specification_(self):
        with self._choice():
            with self._option():
                self._value_specification_()
            with self._option():
                self._token('NONE')
            self._error('expecting one of: NONE')

    @graken
    def _set_local_time_zone_statement_(self):
        self._token('SET')
        self._token('TIME')
        self._token('ZONE')
        self._set_time_zone_value_()

    @graken
    def _set_time_zone_value_(self):
        with self._choice():
            with self._option():
                self._interval_value_expression_()
            with self._option():
                self._token('LOCAL')
            self._error('expecting one of: LOCAL')

    @graken
    def _set_catalog_statement_(self):
        self._token('SET')
        self._token('CATALOG')
        self._value_specification_()

    @graken
    def _set_schema_statement_(self):
        self._token('SET')
        self._token('SCHEMA')
        self._value_specification_()

    @graken
    def _set_names_statement_(self):
        self._token('SET')
        self._token('NAMES')
        self._value_specification_()

    @graken
    def _set_path_statement_(self):
        self._token('SET')
        self._token('PATH')
        self._value_specification_()

    @graken
    def _set_transform_group_statement_(self):
        self._token('SET')
        self._transform_group_characteristic_()

    @graken
    def _transform_group_characteristic_(self):
        with self._choice():
            with self._option():
                self._token('DEFAULT')
                self._token('TRANSFORM')
                self._token('GROUP')
                self._value_specification_()
            with self._option():
                self._token('TRANSFORM')
                self._token('GROUP')
                self._token('FOR')
                self._token('TYPE')
                self._path_resolved_user_defined_type_name_()
                self._value_specification_()
            self._error('no available options')

    @graken
    def _set_session_collation_statement_(self):
        with self._choice():
            with self._option():
                self._token('SET')
                self._token('COLLATION')
                self._collation_specification_()
                with self._optional():
                    self._token('FOR')
                    self._character_set_specification_list_()
            with self._option():
                self._token('SET')
                self._token('NO')
                self._token('COLLATION')
                with self._optional():
                    self._token('FOR')
                    self._character_set_specification_list_()
            self._error('expecting one of: SET')

    @graken
    def _collation_specification_(self):
        self._value_specification_()

    @graken
    def _allocate_descriptor_statement_(self):
        self._token('ALLOCATE')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()
        with self._optional():
            self._token('WITH')
            self._token('MAX')
            self._occurrences_()

    @graken
    def _occurrences_(self):
        self._simple_value_specification_()

    @graken
    def _deallocate_descriptor_statement_(self):
        self._token('DEALLOCATE')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()

    @graken
    def _get_descriptor_statement_(self):
        self._token('GET')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()
        self._get_descriptor_information_()

    @graken
    def _get_descriptor_information_(self):
        with self._choice():
            with self._option():
                def sep0():
                    self._token(',')

                def block0():
                    self._get_header_information_()

                self._positive_closure(block0, prefix=sep0)
            with self._option():
                self._token('VALUE')
                self._item_number_()

                def sep1():
                    self._token(',')

                def block1():
                    self._get_item_information_()

                self._positive_closure(block1, prefix=sep1)
            self._error('no available options')

    @graken
    def _get_header_information_(self):
        self._simple_target_specification_()
        self._token('=')
        self._header_item_name_()

    @graken
    def _header_item_name_(self):
        with self._choice():
            with self._option():
                self._token('COUNT')
            with self._option():
                self._token('KEY_TYPE')
            with self._option():
                self._token('DYNAMIC_FUNCTION')
            with self._option():
                self._token('DYNAMIC_FUNCTION_CODE')
            with self._option():
                self._token('TOP_LEVEL_COUNT')
            self._error('expecting one of: COUNT DYNAMIC_FUNCTION '
                        'DYNAMIC_FUNCTION_CODE KEY_TYPE TOP_LEVEL_COUNT')

    @graken
    def _get_item_information_(self):
        self._simple_target_specification_()
        self._token('=')
        self._descriptor_item_name_()

    @graken
    def _item_number_(self):
        self._simple_value_specification_()

    @graken
    def _descriptor_item_name_(self):
        with self._choice():
            with self._option():
                self._token('CARDINALITY')
            with self._option():
                self._token('CHARACTER_SET_CATALOG')
            with self._option():
                self._token('CHARACTER_SET_NAME')
            with self._option():
                self._token('CHARACTER_SET_SCHEMA')
            with self._option():
                self._token('COLLATION_CATALOG')
            with self._option():
                self._token('COLLATION_NAME')
            with self._option():
                self._token('COLLATION_SCHEMA')
            with self._option():
                self._token('DATA')
            with self._option():
                self._token('DATETIME_INTERVAL_CODE')
            with self._option():
                self._token('DATETIME_INTERVAL_PRECISION')
            with self._option():
                self._token('DEGREE')
            with self._option():
                self._token('INDICATOR')
            with self._option():
                self._token('KEY_MEMBER')
            with self._option():
                self._token('LENGTH')
            with self._option():
                self._token('LEVEL')
            with self._option():
                self._token('NAME')
            with self._option():
                self._token('NULLABLE')
            with self._option():
                self._token('OCTET_LENGTH')
            with self._option():
                self._token('PARAMETER_MODE')
            with self._option():
                self._token('PARAMETER_ORDINAL_POSITION')
            with self._option():
                self._token('PARAMETER_SPECIFIC_CATALOG')
            with self._option():
                self._token('PARAMETER_SPECIFIC_NAME')
            with self._option():
                self._token('PARAMETER_SPECIFIC_SCHEMA')
            with self._option():
                self._token('PRECISION')
            with self._option():
                self._token('RETURNED_CARDINALITY')
            with self._option():
                self._token('RETURNED_LENGTH')
            with self._option():
                self._token('RETURNED_OCTET_LENGTH')
            with self._option():
                self._token('SCALE')
            with self._option():
                self._token('SCOPE_CATALOG')
            with self._option():
                self._token('SCOPE_NAME')
            with self._option():
                self._token('SCOPE_SCHEMA')
            with self._option():
                self._token('TYPE')
            with self._option():
                self._token('UNNAMED')
            with self._option():
                self._token('USER_DEFINED_TYPE_CATALOG')
            with self._option():
                self._token('USER_DEFINED_TYPE_NAME')
            with self._option():
                self._token('USER_DEFINED_TYPE_SCHEMA')
            with self._option():
                self._token('USER_DEFINED_TYPE_CODE')
            self._error('expecting one of: CARDINALITY CHARACTER_SET_CATALOG '
                        'CHARACTER_SET_NAME CHARACTER_SET_SCHEMA '
                        'COLLATION_CATALOG COLLATION_NAME COLLATION_SCHEMA '
                        'DATA DATETIME_INTERVAL_CODE '
                        'DATETIME_INTERVAL_PRECISION DEGREE INDICATOR '
                        'KEY_MEMBER LENGTH LEVEL NAME NULLABLE OCTET_LENGTH '
                        'PARAMETER_MODE PARAMETER_ORDINAL_POSITION '
                        'PARAMETER_SPECIFIC_CATALOG PARAMETER_SPECIFIC_NAME '
                        'PARAMETER_SPECIFIC_SCHEMA PRECISION '
                        'RETURNED_CARDINALITY RETURNED_LENGTH '
                        'RETURNED_OCTET_LENGTH SCALE SCOPE_CATALOG SCOPE_NAME '
                        'SCOPE_SCHEMA TYPE UNNAMED USER_DEFINED_TYPE_CATALOG '
                        'USER_DEFINED_TYPE_CODE USER_DEFINED_TYPE_NAME '
                        'USER_DEFINED_TYPE_SCHEMA')

    @graken
    def _set_descriptor_statement_(self):
        self._token('SET')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()
        self._set_descriptor_information_()

    @graken
    def _set_descriptor_information_(self):
        with self._choice():
            with self._option():
                def sep0():
                    self._token(',')

                def block0():
                    self._set_header_information_()

                self._positive_closure(block0, prefix=sep0)
            with self._option():
                self._token('VALUE')
                self._item_number_()

                def sep1():
                    self._token(',')

                def block1():
                    self._set_item_information_()

                self._positive_closure(block1, prefix=sep1)
            self._error('no available options')

    @graken
    def _set_header_information_(self):
        self._header_item_name_()
        self._token('=')
        self._simple_value_specification_()

    @graken
    def _set_item_information_(self):
        self._descriptor_item_name_()
        self._token('=')
        self._simple_value_specification_()

    @graken
    def _prepare_statement_(self):
        self._token('PREPARE')
        self._sql_statement_name_()
        with self._optional():
            self._attributes_specification_()
        self._token('FROM')
        self._sql_statement_variable_()

    @graken
    def _attributes_specification_(self):
        self._token('ATTRIBUTES')
        self._attributes_variable_()

    @graken
    def _attributes_variable_(self):
        self._simple_value_specification_()

    @graken
    def _sql_statement_variable_(self):
        self._simple_value_specification_()

    @graken
    def _deallocate_prepared_statement_(self):
        self._token('DEALLOCATE')
        self._token('PREPARE')
        self._sql_statement_name_()

    @graken
    def _describe_statement_(self):
        with self._choice():
            with self._option():
                self._describe_input_statement_()
            with self._option():
                self._describe_output_statement_()
            self._error('no available options')

    @graken
    def _describe_input_statement_(self):
        self._token('DESCRIBE')
        self._token('INPUT')
        self._sql_statement_name_()
        self._using_descriptor_()
        with self._optional():
            self._nesting_option_()

    @graken
    def _describe_output_statement_(self):
        self._token('DESCRIBE')
        with self._optional():
            self._token('OUTPUT')
        self._described_object_()
        self._using_descriptor_()
        with self._optional():
            self._nesting_option_()

    @graken
    def _nesting_option_(self):
        with self._choice():
            with self._option():
                self._token('WITH')
                self._token('NESTING')
            with self._option():
                self._token('WITHOUT')
                self._token('NESTING')
            self._error('expecting one of: WITH WITHOUT')

    @graken
    def _using_descriptor_(self):
        self._token('USING')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()

    @graken
    def _described_object_(self):
        with self._choice():
            with self._option():
                self._sql_statement_name_()
            with self._option():
                self._token('CURSOR')
                self._extended_cursor_name_()
                self._token('STRUCTURE')
            self._error('no available options')

    @graken
    def _input_using_clause_(self):
        with self._choice():
            with self._option():
                self._using_arguments_()
            with self._option():
                self._using_descriptor_()
            self._error('no available options')

    @graken
    def _using_arguments_(self):
        self._token('USING')

        def sep0():
            self._token(',')

        def block0():
            self._using_argument_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _using_argument_(self):
        self._general_value_specification_()

    @graken
    def _output_using_clause_(self):
        with self._choice():
            with self._option():
                self._into_arguments_()
            with self._option():
                self._into_descriptor_()
            self._error('no available options')

    @graken
    def _into_arguments_(self):
        self._token('INTO')

        def sep0():
            self._token(',')

        def block0():
            self._target_specification_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _into_descriptor_(self):
        self._token('INTO')
        with self._optional():
            self._token('SQL')
        self._token('DESCRIPTOR')
        self._descriptor_name_()

    @graken
    def _execute_statement_(self):
        self._token('EXECUTE')
        self._sql_statement_name_()
        with self._optional():
            self._result_using_clause_()
        with self._optional():
            self._parameter_using_clause_()

    @graken
    def _result_using_clause_(self):
        self._output_using_clause_()

    @graken
    def _parameter_using_clause_(self):
        self._input_using_clause_()

    @graken
    def _execute_immediate_statement_(self):
        self._token('EXECUTE')
        self._token('IMMEDIATE')
        self._sql_statement_variable_()

    @graken
    def _allocate_cursor_statement_(self):
        self._token('ALLOCATE')
        self._extended_cursor_name_()
        self._cursor_intent_()

    @graken
    def _cursor_intent_(self):
        with self._choice():
            with self._option():
                self._statement_cursor_()
            with self._option():
                self._result_set_cursor_()
            self._error('no available options')

    @graken
    def _statement_cursor_(self):
        with self._optional():
            self._cursor_sensitivity_()
        with self._optional():
            self._cursor_scrollability_()
        self._token('CURSOR')
        with self._optional():
            self._cursor_holdability_()
        with self._optional():
            self._cursor_returnability_()
        self._token('FOR')
        self._extended_statement_name_()

    @graken
    def _result_set_cursor_(self):
        self._token('FOR')
        self._token('PROCEDURE')
        self._specific_routine_designator_()

    @graken
    def _dynamic_open_statement_(self):
        self._token('OPEN')
        self._dynamic_cursor_name_()
        with self._optional():
            self._input_using_clause_()

    @graken
    def _dynamic_fetch_statement_(self):
        self._token('FETCH')
        with self._optional():
            with self._optional():
                self._fetch_orientation_()
            self._token('FROM')
        self._dynamic_cursor_name_()
        self._output_using_clause_()

    @graken
    def _dynamic_close_statement_(self):
        self._token('CLOSE')
        self._dynamic_cursor_name_()

    @graken
    def _dynamic_delete_statement_positioned_(self):
        self._token('DELETE')
        self._token('FROM')
        self._target_table_()
        self._token('WHERE')
        self._token('CURRENT')
        self._token('OF')
        self._dynamic_cursor_name_()

    @graken
    def _dynamic_update_statement_positioned_(self):
        self._token('UPDATE')
        self._target_table_()
        self._token('SET')
        self._set_clause_list_()
        self._token('WHERE')
        self._token('CURRENT')
        self._token('OF')
        self._dynamic_cursor_name_()

    @graken
    def _direct_sql_statement_(self):
        def sep0():
            self._token(';')

        def block0():
            self._directly_executable_statement_()

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token(';')

    @graken
    def _directly_executable_statement_(self):
        with self._choice():
            with self._option():
                self._direct_sql_data_statement_()
            with self._option():
                self._sql_schema_statement_()
            with self._option():
                self._sql_transaction_statement_()
            with self._option():
                self._sql_connection_statement_()
            with self._option():
                self._sql_session_statement_()
            self._error('no available options')

    @graken
    def _direct_sql_data_statement_(self):
        with self._choice():
            with self._option():
                self._delete_statement_searched_()
            with self._option():
                self._direct_select_statement_multiple_rows_()
            with self._option():
                self._insert_statement_()
            with self._option():
                self._update_statement_searched_()
            with self._option():
                self._merge_statement_()
            with self._option():
                self._temporary_table_declaration_()
            self._error('no available options')

    @graken
    def _direct_select_statement_multiple_rows_(self):
        self._query_expression_()
        with self._optional():
            self._order_by_clause_()
        with self._optional():
            self._updatability_clause_()

    @graken
    def _sql_diagnostics_statement_(self):
        self._token('GET')
        self._token('DIAGNOSTICS')
        self._sql_diagnostics_information_()

    @graken
    def _sql_diagnostics_information_(self):
        with self._choice():
            with self._option():
                self._statement_information_()
            with self._option():
                self._condition_information_()
            self._error('no available options')

    @graken
    def _statement_information_(self):
        def sep0():
            self._token(',')

        def block0():
            self._statement_information_item_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _statement_information_item_(self):
        self._simple_target_specification_()
        self._token('=')
        self._statement_information_item_name_()

    @graken
    def _statement_information_item_name_(self):
        with self._choice():
            with self._option():
                self._token('NUMBER')
            with self._option():
                self._token('MORE')
            with self._option():
                self._token('COMMAND_FUNCTION')
            with self._option():
                self._token('COMMAND_FUNCTION_CODE')
            with self._option():
                self._token('DYNAMIC_FUNCTION')
            with self._option():
                self._token('DYNAMIC_FUNCTION_CODE')
            with self._option():
                self._token('ROW_COUNT')
            with self._option():
                self._token('TRANSACTIONS_COMMITTED')
            with self._option():
                self._token('TRANSACTIONS_ROLLED_BACK')
            with self._option():
                self._token('TRANSACTION_ACTIVE')
            self._error('expecting one of: COMMAND_FUNCTION '
                        'COMMAND_FUNCTION_CODE DYNAMIC_FUNCTION '
                        'DYNAMIC_FUNCTION_CODE MORE NUMBER ROW_COUNT '
                        'TRANSACTIONS_COMMITTED TRANSACTIONS_ROLLED_BACK '
                        'TRANSACTION_ACTIVE')

    @graken
    def _condition_information_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('EXCEPTION')
                with self._option():
                    self._token('CONDITION')
                self._error('expecting one of: CONDITION EXCEPTION')
        self._condition_number_()

        def sep1():
            self._token(',')

        def block1():
            self._condition_information_item_()

        self._positive_closure(block1, prefix=sep1)

    @graken
    def _condition_information_item_(self):
        self._simple_target_specification_()
        self._token('=')
        self._condition_information_item_name_()

    @graken
    def _condition_information_item_name_(self):
        with self._choice():
            with self._option():
                self._token('CATALOG_NAME')
            with self._option():
                self._token('CLASS_ORIGIN')
            with self._option():
                self._token('COLUMN_NAME')
            with self._option():
                self._token('CONDITION_NUMBER')
            with self._option():
                self._token('CONNECTION_NAME')
            with self._option():
                self._token('CONSTRAINT_CATALOG')
            with self._option():
                self._token('CONSTRAINT_NAME')
            with self._option():
                self._token('CONSTRAINT_SCHEMA')
            with self._option():
                self._token('CURSOR_NAME')
            with self._option():
                self._token('MESSAGE_LENGTH')
            with self._option():
                self._token('MESSAGE_OCTET_LENGTH')
            with self._option():
                self._token('MESSAGE_TEXT')
            with self._option():
                self._token('PARAMETER_MODE')
            with self._option():
                self._token('PARAMETER_NAME')
            with self._option():
                self._token('PARAMETER_ORDINAL_POSITION')
            with self._option():
                self._token('RETURNED_SQLSTATE')
            with self._option():
                self._token('ROUTINE_CATALOG')
            with self._option():
                self._token('ROUTINE_NAME')
            with self._option():
                self._token('ROUTINE_SCHEMA')
            with self._option():
                self._token('SCHEMA_NAME')
            with self._option():
                self._token('SERVER_NAME')
            with self._option():
                self._token('SPECIFIC_NAME')
            with self._option():
                self._token('SUBCLASS_ORIGIN')
            with self._option():
                self._token('TABLE_NAME')
            with self._option():
                self._token('TRIGGER_CATALOG')
            with self._option():
                self._token('TRIGGER_NAME')
            with self._option():
                self._token('TRIGGER_SCHEMA')
            self._error('expecting one of: CATALOG_NAME CLASS_ORIGIN '
                        'COLUMN_NAME CONDITION_NUMBER CONNECTION_NAME '
                        'CONSTRAINT_CATALOG CONSTRAINT_NAME CONSTRAINT_SCHEMA '
                        'CURSOR_NAME MESSAGE_LENGTH MESSAGE_OCTET_LENGTH '
                        'MESSAGE_TEXT PARAMETER_MODE PARAMETER_NAME '
                        'PARAMETER_ORDINAL_POSITION RETURNED_SQLSTATE '
                        'ROUTINE_CATALOG ROUTINE_NAME ROUTINE_SCHEMA '
                        'SCHEMA_NAME SERVER_NAME SPECIFIC_NAME '
                        'SUBCLASS_ORIGIN TABLE_NAME TRIGGER_CATALOG '
                        'TRIGGER_NAME TRIGGER_SCHEMA')

    @graken
    def _condition_number_(self):
        self._simple_value_specification_()
