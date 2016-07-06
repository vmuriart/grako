#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    def _space_(self):
        self._pattern(r'\s')

    @graken
    def _regular_identifier_(self):
        self._pattern(r'[a-z]\w*')
        self._check_name()

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
    def _integer_(self):
        self._pattern(r'\d+')

    @graken
    def _approximate_numeric_literal_(self):
        self._mantissa_()
        self._token('E')
        self._exponent_()

    @graken
    def _mantissa_(self):
        self._exact_numeric_literal_()

    @graken
    def _exponent_(self):
        self._signed_integer_()

    @graken
    def _signed_integer_(self):
        with self._optional():
            self._sign_()
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
    def _national_character_string_literal_(self):
        self._token('N')
        self._token("'")
        with self._optional():
            def block0():
                self._character_representation_()

            self._positive_closure(block0)
        self._token("'")
        with self._optional():
            def block1():
                def block2():
                    self._separator_()

                self._positive_closure(block2)
                self._token("'")
                with self._optional():
                    def block3():
                        self._character_representation_()

                    self._positive_closure(block3)
                self._token("'")

            self._positive_closure(block1)

    @graken
    def _character_representation_(self):
        with self._choice():
            with self._option():
                self._pattern(r'[a-z]')
            with self._option():
                self._token("''")
            self._error("expecting one of: '' [a-z]")

    @graken
    def _separator_(self):
        def block0():
            self._space_()

        self._positive_closure(block0)

    @graken
    def _bit_string_literal_(self):
        self._token('B')
        self._token("'")
        with self._optional():
            self._bit_()
        self._token("'")
        with self._optional():
            def block0():
                def block1():
                    self._separator_()

                self._positive_closure(block1)
                self._token("'")
                with self._optional():
                    self._bit_()
                self._token("'")

            self._positive_closure(block0)

    @graken
    def _bit_(self):
        self._pattern(r'[01]+')

    @graken
    def _hex_string_literal_(self):
        self._token('X')
        self._token("'")
        with self._optional():
            self._hexit_()
        self._token("'")
        with self._optional():
            def block0():
                def block1():
                    self._separator_()

                self._positive_closure(block1)
                self._token("'")
                with self._optional():
                    self._hexit_()
                self._token("'")

            self._positive_closure(block0)

    @graken
    def _hexit_(self):
        self._pattern(r'[a-f\d]+')

    @graken
    def _character_string_literal_(self):
        with self._optional():
            self._token('_')
            self._character_set_name_()
        self._token("'")
        with self._optional():
            def block0():
                self._character_representation_()

            self._positive_closure(block0)
        self._token("'")
        with self._optional():
            def block1():
                def block2():
                    self._separator_()

                self._positive_closure(block2)
                self._token("'")
                with self._optional():
                    def block3():
                        self._character_representation_()

                    self._positive_closure(block3)
                self._token("'")

            self._positive_closure(block1)

    @graken
    def _character_set_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._regular_identifier_()

    @graken
    def _schema_name_(self):
        with self._optional():
            self._catalog_name_()
            self._token('.')
        self._unqualified_schema_name_()

    @graken
    def _catalog_name_(self):
        self._identifier_()

    @graken
    def _identifier_(self):
        with self._optional():
            self._token('_')
            self._character_set_name_()
        self._actual_identifier_()

    @graken
    def _actual_identifier_(self):
        with self._choice():
            with self._option():
                self._regular_identifier_()
            with self._option():
                self._delimited_identifier_()
            self._error('no available options')

    @graken
    def _delimited_identifier_(self):
        self._token('"')
        self._delimited_identifier_body_()
        self._token('"')

    @graken
    def _delimited_identifier_body_(self):
        def block0():
            self._delimited_identifier_part_()

        self._positive_closure(block0)

    @graken
    def _delimited_identifier_part_(self):
        with self._choice():
            with self._option():
                self._pattern(r'[a-z]')
            with self._option():
                self._token('""')
            self._error('expecting one of: "" [a-z]')

    @graken
    def _unqualified_schema_name_(self):
        self._identifier_()

    @graken
    def _date_string_(self):
        self._token("'")
        self._date_value_()
        self._token("'")

    @graken
    def _date_value_(self):
        self._years_value_()
        self._token('-')
        self._months_value_()
        self._token('-')
        self._days_value_()

    @graken
    def _years_value_(self):
        self._datetime_value_()

    @graken
    def _datetime_value_(self):
        self._integer_()

    @graken
    def _months_value_(self):
        self._datetime_value_()

    @graken
    def _days_value_(self):
        self._datetime_value_()

    @graken
    def _time_string_(self):
        self._token("'")
        self._time_value_()
        with self._optional():
            self._time_zone_interval_()
        self._token("'")

    @graken
    def _time_value_(self):
        self._hours_value_()
        self._token(':')
        self._minutes_value_()
        self._token(':')
        self._seconds_value_()

    @graken
    def _hours_value_(self):
        self._datetime_value_()

    @graken
    def _minutes_value_(self):
        self._datetime_value_()

    @graken
    def _seconds_value_(self):
        self._seconds_integer_value_()
        with self._optional():
            self._token('.')
            with self._optional():
                self._seconds_fraction_()

    @graken
    def _seconds_integer_value_(self):
        self._integer_()

    @graken
    def _seconds_fraction_(self):
        self._integer_()

    @graken
    def _time_zone_interval_(self):
        self._sign_()
        self._hours_value_()
        self._token(':')
        self._minutes_value_()

    @graken
    def _timestamp_string_(self):
        self._token("'")
        self._date_value_()
        self._space_()
        self._time_value_()
        with self._optional():
            self._time_zone_interval_()
        self._token("'")

    @graken
    def _interval_string_(self):
        self._token("'")
        with self._group():
            with self._choice():
                with self._option():
                    self._year_month_literal_()
                with self._option():
                    self._day_time_literal_()
                self._error('no available options')
        self._token("'")

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
            self._space_()
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
    def _authorization_identifier_(self):
        self._identifier_()

    @graken
    def _temporary_table_declaration_(self):
        self._token('DECLARE')
        self._token('LOCAL')
        self._token('TEMPORARY')
        self._token('TABLE')
        self._qualified_local_table_name_()
        self._table_element_list_()
        with self._optional():
            self._token('ON')
            self._token('COMMIT')
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('PRESERVE')
                    with self._option():
                        self._token('DELETE')
                    self._error('expecting one of: DELETE PRESERVE')
            self._token('ROWS')

    @graken
    def _qualified_local_table_name_(self):
        self._token('MODULE')
        self._token('.')
        self._local_table_name_()

    @graken
    def _local_table_name_(self):
        self._qualified_identifier_()

    @graken
    def _qualified_identifier_(self):
        self._identifier_()

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
            self._error('no available options')

    @graken
    def _column_definition_(self):
        self._column_name_()
        with self._group():
            with self._choice():
                with self._option():
                    self._data_type_()
                with self._option():
                    self._domain_name_()
                self._error('no available options')
        with self._optional():
            self._default_clause_()
        with self._optional():
            def block1():
                self._column_constraint_definition_()

            self._positive_closure(block1)
        with self._optional():
            self._collate_clause_()

    @graken
    def _column_name_(self):
        self._identifier_()

    @graken
    def _data_type_(self):
        with self._choice():
            with self._option():
                self._character_string_type_()
                with self._optional():
                    self._token('CHARACTER')
                    self._token('SET')
                    self._character_set_name_()
            with self._option():
                self._national_character_string_type_()
            with self._option():
                self._bit_string_type_()
            with self._option():
                self._numeric_type_()
            with self._option():
                self._datetime_type_()
            with self._option():
                self._interval_type_()
            self._error('no available options')

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
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('CHAR')
                self._token('VARYING')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('VARCHAR')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            self._error('expecting one of: CHAR CHARACTER VARCHAR')

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
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('NATIONAL')
                self._token('CHAR')
                self._token('VARYING')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('NCHAR')
                self._token('VARYING')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            self._error('expecting one of: NATIONAL NCHAR')

    @graken
    def _bit_string_type_(self):
        with self._choice():
            with self._option():
                self._token('BIT')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            with self._option():
                self._token('BIT')
                self._token('VARYING')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
            self._error('expecting one of: BIT')

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
                self._token('INTEGER')
            with self._option():
                self._token('INT')
            with self._option():
                self._token('SMALLINT')
            self._error(
                'expecting one of: DEC DECIMAL INT INTEGER NUMERIC SMALLINT')

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
                self._token('PRECISION')
            self._error('expecting one of: DOUBLE FLOAT REAL')

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
                    self._token('WITH')
                    self._token('TIME')
                    self._token('ZONE')
            with self._option():
                self._token('TIMESTAMP')
                with self._optional():
                    self._token('(')
                    self._integer_()
                    self._token(')')
                with self._optional():
                    self._token('WITH')
                    self._token('TIME')
                    self._token('ZONE')
            self._error('expecting one of: DATE TIME TIMESTAMP')

    @graken
    def _interval_type_(self):
        self._token('INTERVAL')
        self._interval_qualifier_()

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
        self._non_second_datetime_field_()
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _non_second_datetime_field_(self):
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
    def _end_field_(self):
        with self._choice():
            with self._option():
                self._non_second_datetime_field_()
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
                self._non_second_datetime_field_()
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
                        self._token('(')
                        self._integer_()
                    self._token(')')
            self._error('expecting one of: SECOND')

    @graken
    def _domain_name_(self):
        self._qualified_name_()

    @graken
    def _qualified_name_(self):
        with self._optional():
            self._schema_name_()
            self._token('.')
        self._qualified_identifier_()

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
                self._token('SESSION_USER')
            with self._option():
                self._token('SYSTEM_USER')
            with self._option():
                self._token('NULL')
            self._error('expecting one of: CURRENT_USER NULL SESSION_USER '
                        'SYSTEM_USER USER')

    @graken
    def _literal_(self):
        with self._choice():
            with self._option():
                self._signed_numeric_literal_()
            with self._option():
                self._general_literal_()
            self._error('no available options')

    @graken
    def _signed_numeric_literal_(self):
        with self._optional():
            self._sign_()
        self._unsigned_numeric_literal_()

    @graken
    def _general_literal_(self):
        with self._choice():
            with self._option():
                self._character_string_literal_()
            with self._option():
                self._national_character_string_literal_()
            with self._option():
                self._bit_string_literal_()
            with self._option():
                self._hex_string_literal_()
            with self._option():
                self._datetime_literal_()
            with self._option():
                self._interval_literal_()
            self._error('no available options')

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
    def _interval_literal_(self):
        self._token('INTERVAL')
        with self._optional():
            self._sign_()
        self._interval_string_()
        self._interval_qualifier_()

    @graken
    def _datetime_value_function_(self):
        with self._choice():
            with self._option():
                self._current_date_value_function_()
            with self._option():
                self._current_time_value_function_()
            with self._option():
                self._current_timestamp_value_function_()
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
    def _current_timestamp_value_function_(self):
        self._token('CURRENT_TIMESTAMP')
        with self._optional():
            self._token('(')
            self._integer_()
            self._token(')')

    @graken
    def _column_constraint_definition_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._column_constraint_()
        with self._optional():
            self._constraint_attributes_()

    @graken
    def _constraint_name_definition_(self):
        self._token('CONSTRAINT')
        self._constraint_name_()

    @graken
    def _constraint_name_(self):
        self._qualified_name_()

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
    def _unique_specification_(self):
        with self._choice():
            with self._option():
                self._token('UNIQUE')
            with self._option():
                self._token('PRIMARY')
                self._token('KEY')
            self._error('expecting one of: PRIMARY UNIQUE')

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
    def _referenced_table_and_columns_(self):
        self._table_name_()
        with self._optional():
            self._token('(')
            self._reference_column_list_()
            self._token(')')

    @graken
    def _table_name_(self):
        with self._choice():
            with self._option():
                self._qualified_name_()
            with self._option():
                self._qualified_local_table_name_()
            self._error('no available options')

    @graken
    def _reference_column_list_(self):
        self._column_name_list_()

    @graken
    def _column_name_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._column_name_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _match_type_(self):
        with self._choice():
            with self._option():
                self._token('FULL')
            with self._option():
                self._token('PARTIAL')
            self._error('expecting one of: FULL PARTIAL')

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
                self._token('NO')
                self._token('ACTION')
            self._error('expecting one of: CASCADE NO SET')

    @graken
    def _delete_rule_(self):
        self._token('ON')
        self._token('DELETE')
        self._referential_action_()

    @graken
    def _check_constraint_definition_(self):
        self._token('CHECK')
        self._token('(')
        self._search_condition_()
        self._token(')')

    @graken
    def _search_condition_(self):
        with self._choice():
            with self._option():
                self._boolean_term_()
            with self._option():
                self._search_condition_()
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
    def _boolean_primary_(self):
        with self._choice():
            with self._option():
                self._predicate_()
            with self._option():
                self._token('(')
                self._search_condition_()
                self._token(')')
            self._error('no available options')

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
                self._null_predicate_()
            with self._option():
                self._quantified_comparison_predicate_()
            with self._option():
                self._exists_predicate_()
            with self._option():
                self._match_predicate_()
            with self._option():
                self._overlaps_predicate_()
            self._error('no available options')

    @graken
    def _comparison_predicate_(self):
        self._row_value_constructor_()
        self._comp_op_()
        self._row_value_constructor_()

    @graken
    def _row_value_constructor_(self):
        with self._choice():
            with self._option():
                self._row_value_constructor_element_()
            with self._option():
                self._token('(')
                self._row_value_constructor_list_()
                self._token(')')
            with self._option():
                self._row_subquery_()
            self._error('no available options')

    @graken
    def _row_value_constructor_element_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._token('NULL')
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT NULL')

    @graken
    def _value_expression_(self):
        with self._choice():
            with self._option():
                self._numeric_value_expression_()
            with self._option():
                self._string_value_expression_()
            with self._option():
                self._datetime_value_expression_()
            with self._option():
                self._interval_value_expression_()
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
    def _value_expression_primary_(self):
        with self._choice():
            with self._option():
                self._unsigned_value_specification_()
            with self._option():
                self._column_reference_()
            with self._option():
                self._set_function_specification_()
            with self._option():
                self._scalar_subquery_()
            with self._option():
                self._case_expression_()
            with self._option():
                self._token('(')
                self._value_expression_()
                self._token(')')
            with self._option():
                self._cast_specification_()
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
    def _unsigned_literal_(self):
        with self._choice():
            with self._option():
                self._unsigned_numeric_literal_()
            with self._option():
                self._general_literal_()
            self._error('no available options')

    @graken
    def _general_value_specification_(self):
        with self._choice():
            with self._option():
                self._parameter_specification_()
            with self._option():
                self._token('?')
            with self._option():
                self._token('USER')
            with self._option():
                self._token('CURRENT_USER')
            with self._option():
                self._token('SESSION_USER')
            with self._option():
                self._token('SYSTEM_USER')
            with self._option():
                self._token('VALUE')
            self._error('expecting one of: ? CURRENT_USER SESSION_USER '
                        'SYSTEM_USER USER VALUE')

    @graken
    def _parameter_specification_(self):
        self._parameter_name_()
        with self._optional():
            self._indicator_parameter_()

    @graken
    def _parameter_name_(self):
        self._token(':')
        self._identifier_()

    @graken
    def _indicator_parameter_(self):
        with self._optional():
            self._token('INDICATOR')
        self._parameter_name_()

    @graken
    def _column_reference_(self):
        with self._optional():
            self._qualifier_()
            self._token('.')
        self._column_name_()

    @graken
    def _qualifier_(self):
        with self._choice():
            with self._option():
                self._table_name_()
            with self._option():
                self._correlation_name_()
            self._error('no available options')

    @graken
    def _correlation_name_(self):
        self._identifier_()

    @graken
    def _set_function_specification_(self):
        with self._choice():
            with self._option():
                self._token('COUNT')
                self._token('(')
                self._token('*')
                self._token(')')
            with self._option():
                self._general_set_function_()
            self._error('expecting one of: COUNT')

    @graken
    def _general_set_function_(self):
        self._set_function_type_()
        self._token('(')
        with self._optional():
            self._set_quantifier_()
        self._value_expression_()
        self._token(')')

    @graken
    def _set_function_type_(self):
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
                self._token('COUNT')
            self._error('expecting one of: AVG COUNT MAX MIN SUM')

    @graken
    def _set_quantifier_(self):
        with self._choice():
            with self._option():
                self._token('DISTINCT')
            with self._option():
                self._token('ALL')
            self._error('expecting one of: ALL DISTINCT')

    @graken
    def _scalar_subquery_(self):
        self._subquery_()

    @graken
    def _subquery_(self):
        self._token('(')
        self._query_expression_()
        self._token(')')

    @graken
    def _query_expression_(self):
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
                self._query_expression_()
                self._token('UNION')
                with self._optional():
                    self._token('ALL')
                with self._optional():
                    self._corresponding_spec_()
                self._query_term_()
            with self._option():
                self._query_expression_()
                self._token('EXCEPT')
                with self._optional():
                    self._token('ALL')
                with self._optional():
                    self._corresponding_spec_()
                self._query_term_()
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
                    self._token('ALL')
                with self._optional():
                    self._corresponding_spec_()
                self._query_primary_()
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
                self._qualifier_()
                self._token('.')
                self._token('*')
            self._error('no available options')

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
    def _table_expression_(self):
        self._from_clause_()
        with self._optional():
            self._where_clause_()
        with self._optional():
            self._group_by_clause_()
        with self._optional():
            self._having_clause_()

    @graken
    def _from_clause_(self):
        self._token('FROM')

        def sep0():
            self._token(',')

        def block0():
            self._table_reference_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _table_reference_(self):
        with self._choice():
            with self._option():
                self._table_name_()
                with self._optional():
                    self._correlation_specification_()
            with self._option():
                self._derived_table_()
                self._correlation_specification_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _correlation_specification_(self):
        with self._optional():
            self._token('AS')
        self._correlation_name_()
        with self._optional():
            self._token('(')
            self._derived_column_list_()
            self._token(')')

    @graken
    def _derived_column_list_(self):
        self._column_name_list_()

    @graken
    def _derived_table_(self):
        self._table_subquery_()

    @graken
    def _table_subquery_(self):
        self._subquery_()

    @graken
    def _joined_table_(self):
        with self._choice():
            with self._option():
                self._cross_join_()
            with self._option():
                self._qualified_join_()
            with self._option():
                self._token('(')
                self._joined_table_()
                self._token(')')
            self._error('no available options')

    @graken
    def _cross_join_(self):
        self._table_reference_()
        self._token('CROSS')
        self._token('JOIN')
        self._table_reference_()

    @graken
    def _qualified_join_(self):
        self._table_reference_()
        with self._optional():
            self._token('NATURAL')
        with self._optional():
            self._join_type_()
        self._token('JOIN')
        self._table_reference_()
        with self._optional():
            self._join_specification_()

    @graken
    def _join_type_(self):
        with self._choice():
            with self._option():
                self._token('INNER')
            with self._option():
                self._outer_join_type_()
                with self._optional():
                    self._token('OUTER')
            with self._option():
                self._token('UNION')
            self._error('expecting one of: INNER UNION')

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
        self._join_column_list_()
        self._token(')')

    @graken
    def _join_column_list_(self):
        self._column_name_list_()

    @graken
    def _where_clause_(self):
        self._token('WHERE')
        self._search_condition_()

    @graken
    def _group_by_clause_(self):
        self._token('GROUP')
        self._token('BY')
        self._grouping_column_reference_list_()

    @graken
    def _grouping_column_reference_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._grouping_column_reference_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _grouping_column_reference_(self):
        self._column_reference_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _collate_clause_(self):
        self._token('COLLATE')
        self._collation_name_()

    @graken
    def _collation_name_(self):
        self._qualified_name_()

    @graken
    def _having_clause_(self):
        self._token('HAVING')
        self._search_condition_()

    @graken
    def _table_value_constructor_(self):
        self._token('VALUES')
        self._table_value_constructor_list_()

    @graken
    def _table_value_constructor_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._row_value_constructor_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _explicit_table_(self):
        self._token('TABLE')
        self._table_name_()

    @graken
    def _query_term_(self):
        with self._choice():
            with self._option():
                self._non_join_query_term_()
            with self._option():
                self._joined_table_()
            self._error('no available options')

    @graken
    def _corresponding_spec_(self):
        self._token('CORRESPONDING')
        with self._optional():
            self._token('BY')
            self._token('(')
            self._corresponding_column_list_()
            self._token(')')

    @graken
    def _corresponding_column_list_(self):
        self._column_name_list_()

    @graken
    def _query_primary_(self):
        with self._choice():
            with self._option():
                self._non_join_query_primary_()
            with self._option():
                self._joined_table_()
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
    def _case_operand_(self):
        self._value_expression_()

    @graken
    def _simple_when_clause_(self):
        self._token('WHEN')
        self._when_operand_()
        self._token('THEN')
        self._result_()

    @graken
    def _when_operand_(self):
        self._value_expression_()

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
    def _else_clause_(self):
        self._token('ELSE')
        self._result_()

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
    def _searched_when_clause_(self):
        self._token('WHEN')
        self._search_condition_()
        self._token('THEN')
        self._result_()

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
                self._token('NULL')
            self._error('expecting one of: NULL')

    @graken
    def _cast_target_(self):
        with self._choice():
            with self._option():
                self._domain_name_()
            with self._option():
                self._data_type_()
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
            self._error('no available options')

    @graken
    def _position_expression_(self):
        self._token('POSITION')
        self._token('(')
        self._character_value_expression_()
        self._token('IN')
        self._character_value_expression_()
        self._token(')')

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
    def _string_value_function_(self):
        with self._choice():
            with self._option():
                self._character_value_function_()
            with self._option():
                self._bit_value_function_()
            self._error('no available options')

    @graken
    def _character_value_function_(self):
        with self._choice():
            with self._option():
                self._character_substring_function_()
            with self._option():
                self._fold_()
            with self._option():
                self._form_of_use_conversion_()
            with self._option():
                self._character_translation_()
            with self._option():
                self._trim_function_()
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
        self._token(')')

    @graken
    def _start_position_(self):
        self._numeric_value_expression_()

    @graken
    def _string_length_(self):
        self._numeric_value_expression_()

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
    def _form_of_use_conversion_(self):
        self._token('CONVERT')
        self._token('(')
        self._character_value_expression_()
        self._token('USING')
        self._form_of_use_conversion_name_()
        self._token(')')

    @graken
    def _form_of_use_conversion_name_(self):
        self._qualified_name_()

    @graken
    def _character_translation_(self):
        self._token('TRANSLATE')
        self._token('(')
        self._character_value_expression_()
        self._token('USING')
        self._translation_name_()
        self._token(')')

    @graken
    def _translation_name_(self):
        self._qualified_name_()

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
    def _trim_source_(self):
        self._character_value_expression_()

    @graken
    def _bit_value_function_(self):
        self._bit_substring_function_()

    @graken
    def _bit_substring_function_(self):
        self._token('SUBSTRING')
        self._token('(')
        self._bit_value_expression_()
        self._token('FROM')
        self._start_position_()
        with self._optional():
            self._token('FOR')
            self._string_length_()
        self._token(')')

    @graken
    def _bit_value_expression_(self):
        with self._choice():
            with self._option():
                self._bit_concatenation_()
            with self._option():
                self._bit_factor_()
            self._error('no available options')

    @graken
    def _bit_concatenation_(self):
        self._bit_value_expression_()
        self._token('||')
        self._bit_factor_()

    @graken
    def _bit_factor_(self):
        self._bit_primary_()

    @graken
    def _bit_primary_(self):
        with self._choice():
            with self._option():
                self._value_expression_primary_()
            with self._option():
                self._string_value_function_()
            self._error('no available options')

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
                self._datetime_field_()
            with self._option():
                self._time_zone_field_()
            self._error('no available options')

    @graken
    def _datetime_field_(self):
        with self._choice():
            with self._option():
                self._non_second_datetime_field_()
            with self._option():
                self._token('SECOND')
            self._error('expecting one of: SECOND')

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
    def _interval_term_(self):
        with self._choice():
            with self._option():
                self._interval_factor_()
            with self._option():
                self._interval_term_2_()
                self._token('*')
                self._factor_()
            with self._option():
                self._interval_term_2_()
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
        self._value_expression_primary_()
        with self._optional():
            self._interval_qualifier_()

    @graken
    def _interval_term_2_(self):
        self._interval_term_()

    @graken
    def _interval_value_expression_(self):
        with self._choice():
            with self._option():
                self._interval_term_()
            with self._option():
                self._interval_value_expression_1_()
                self._token('+')
                self._interval_term_1_()
            with self._option():
                self._interval_value_expression_1_()
                self._token('-')
                self._interval_term_1_()
            with self._option():
                self._token('(')
                self._datetime_value_expression_()
                self._token('-')
                self._datetime_term_()
                self._token(')')
                self._interval_qualifier_()
            self._error('no available options')

    @graken
    def _interval_value_expression_1_(self):
        self._interval_value_expression_()

    @graken
    def _interval_term_1_(self):
        self._interval_term_()

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
                self._interval_value_expression_()
            self._error('expecting one of: LOCAL')

    @graken
    def _length_expression_(self):
        with self._choice():
            with self._option():
                self._char_length_expression_()
            with self._option():
                self._octet_length_expression_()
            with self._option():
                self._bit_length_expression_()
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
        self._token(')')

    @graken
    def _string_value_expression_(self):
        with self._choice():
            with self._option():
                self._character_value_expression_()
            with self._option():
                self._bit_value_expression_()
            self._error('no available options')

    @graken
    def _octet_length_expression_(self):
        self._token('OCTET_LENGTH')
        self._token('(')
        self._string_value_expression_()
        self._token(')')

    @graken
    def _bit_length_expression_(self):
        self._token('BIT_LENGTH')
        self._token('(')
        self._string_value_expression_()
        self._token(')')

    @graken
    def _row_value_constructor_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._row_value_constructor_element_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _row_subquery_(self):
        self._subquery_()

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
        self._row_value_constructor_()
        with self._optional():
            self._token('NOT')
        self._token('BETWEEN')
        self._row_value_constructor_()
        self._token('AND')
        self._row_value_constructor_()

    @graken
    def _in_predicate_(self):
        self._row_value_constructor_()
        with self._optional():
            self._token('NOT')
        self._token('IN')
        self._in_predicate_value_()

    @graken
    def _in_predicate_value_(self):
        with self._choice():
            with self._option():
                self._table_subquery_()
            with self._option():
                self._token('(')
                self._in_value_list_()
                self._token(')')
            self._error('no available options')

    @graken
    def _in_value_list_(self):
        self._value_expression_()

        def block0():
            self._token(',')
            self._value_expression_()

        self._positive_closure(block0)

    @graken
    def _like_predicate_(self):
        self._match_value_()
        with self._optional():
            self._token('NOT')
        self._token('LIKE')
        self._pattern_()
        with self._optional():
            self._token('ESCAPE')
            self._escape_character_()

    @graken
    def _match_value_(self):
        self._character_value_expression_()

    @graken
    def _pattern_(self):
        self._character_value_expression_()

    @graken
    def _escape_character_(self):
        self._character_value_expression_()

    @graken
    def _null_predicate_(self):
        self._token('IS')
        with self._optional():
            self._token('NOT')
        self._token('NULL')

    @graken
    def _quantified_comparison_predicate_(self):
        self._row_value_constructor_()
        self._comp_op_()
        self._quantifier_()
        self._table_subquery_()

    @graken
    def _quantifier_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
            with self._option():
                self._some_()
            self._error('expecting one of: ALL')

    @graken
    def _some_(self):
        with self._choice():
            with self._option():
                self._token('SOME')
            with self._option():
                self._token('ANY')
            self._error('expecting one of: ANY SOME')

    @graken
    def _exists_predicate_(self):
        self._token('EXISTS')
        self._table_subquery_()

    @graken
    def _match_predicate_(self):
        self._row_value_constructor_()
        self._token('MATCH')
        with self._optional():
            self._token('UNIQUE')
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('PARTIAL')
                with self._option():
                    self._token('FULL')
                self._error('expecting one of: FULL PARTIAL')
        self._table_subquery_()

    @graken
    def _overlaps_predicate_(self):
        self._row_value_constructor_1_()
        self._token('OVERLAPS')
        self._row_value_constructor_2_()

    @graken
    def _row_value_constructor_1_(self):
        self._row_value_constructor_()

    @graken
    def _row_value_constructor_2_(self):
        self._row_value_constructor_()

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
    def _constraint_attributes_(self):
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
    def _table_constraint_definition_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._table_constraint_()
        with self._optional():
            self._constraint_check_time_()

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
        self._unique_specification_()
        self._token('(')
        self._unique_column_list_()
        self._token(')')

    @graken
    def _unique_column_list_(self):
        self._column_name_list_()

    @graken
    def _referential_constraint_definition_(self):
        self._token('FOREIGN')
        self._token('KEY')
        self._token('(')
        self._referencing_columns_()
        self._token(')')
        self._references_specification_()

    @graken
    def _referencing_columns_(self):
        self._reference_column_list_()

    @graken
    def _order_by_clause_(self):
        self._token('ORDER')
        self._token('BY')
        self._sort_specification_list_()

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
            self._collate_clause_()
        with self._optional():
            self._ordering_specification_()

    @graken
    def _sort_key_(self):
        with self._choice():
            with self._option():
                self._column_name_()
            with self._option():
                self._integer_()
            self._error('no available options')

    @graken
    def _ordering_specification_(self):
        with self._choice():
            with self._option():
                self._token('ASC')
            with self._option():
                self._token('DESC')
            self._error('expecting one of: ASC DESC')

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
                self._grant_statement_()
            with self._option():
                self._domain_definition_()
            with self._option():
                self._character_set_definition_()
            with self._option():
                self._collation_definition_()
            with self._option():
                self._translation_definition_()
            with self._option():
                self._assertion_definition_()
            self._error('no available options')

    @graken
    def _schema_definition_(self):
        self._token('CREATE')
        self._token('SCHEMA')
        self._schema_name_clause_()
        with self._optional():
            self._schema_character_set_specification_()
        with self._optional():
            def block0():
                self._schema_element_()

            self._positive_closure(block0)

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
    def _schema_element_(self):
        with self._choice():
            with self._option():
                self._domain_definition_()
            with self._option():
                self._table_definition_()
            with self._option():
                self._view_definition_()
            with self._option():
                self._grant_statement_()
            with self._option():
                self._assertion_definition_()
            with self._option():
                self._character_set_definition_()
            with self._option():
                self._collation_definition_()
            with self._option():
                self._translation_definition_()
            self._error('no available options')

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
            self._domain_constraint_()
        with self._optional():
            self._collate_clause_()

    @graken
    def _domain_constraint_(self):
        with self._optional():
            self._constraint_name_definition_()
        self._check_constraint_definition_()
        with self._optional():
            self._constraint_attributes_()

    @graken
    def _table_definition_(self):
        self._token('CREATE')
        with self._optional():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('GLOBAL')
                    with self._option():
                        self._token('LOCAL')
                    self._error('expecting one of: GLOBAL LOCAL')
            self._token('TEMPORARY')
        self._token('TABLE')
        self._table_name_()
        self._table_element_list_()
        with self._optional():
            self._token('ON')
            self._token('COMMIT')
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('DELETE')
                    with self._option():
                        self._token('PRESERVE')
                    self._error('expecting one of: DELETE PRESERVE')
            self._token('ROWS')

    @graken
    def _view_definition_(self):
        self._token('CREATE')
        self._token('VIEW')
        self._table_name_()
        with self._optional():
            self._token('(')
            self._view_column_list_()
            self._token(')')
        self._token('AS')
        self._query_expression_()
        with self._optional():
            self._token('WITH')
            with self._optional():
                self._levels_clause_()
            self._token('CHECK')
            self._token('OPTION')

    @graken
    def _view_column_list_(self):
        self._column_name_list_()

    @graken
    def _levels_clause_(self):
        with self._choice():
            with self._option():
                self._token('CASCADED')
            with self._option():
                self._token('LOCAL')
            self._error('expecting one of: CASCADED LOCAL')

    @graken
    def _grant_statement_(self):
        self._token('GRANT')
        self._privileges_()
        self._token('ON')
        self._object_name_()
        self._token('TO')

        def sep0():
            self._token(',')

        def block0():
            self._grantee_()

        self._positive_closure(block0, prefix=sep0)
        with self._optional():
            self._token('WITH')
            self._token('GRANT')
            self._token('OPTION')

    @graken
    def _privileges_(self):
        with self._choice():
            with self._option():
                self._token('ALL')
                self._token('PRIVILEGES')
            with self._option():
                self._action_list_()
            self._error('expecting one of: ALL')

    @graken
    def _action_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._action_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _action_(self):
        with self._choice():
            with self._option():
                self._token('SELECT')
            with self._option():
                self._token('DELETE')
            with self._option():
                self._token('INSERT')
                with self._optional():
                    self._token('(')
                    self._privilege_column_list_()
                    self._token(')')
            with self._option():
                self._token('UPDATE')
                with self._optional():
                    self._token('(')
                    self._privilege_column_list_()
                    self._token(')')
            with self._option():
                self._token('REFERENCES')
                with self._optional():
                    self._token('(')
                    self._privilege_column_list_()
                    self._token(')')
            with self._option():
                self._token('USAGE')
            self._error('expecting one of: DELETE INSERT REFERENCES SELECT '
                        'UPDATE USAGE')

    @graken
    def _privilege_column_list_(self):
        self._column_name_list_()

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
                self._translation_name_()
            self._error('no available options')

    @graken
    def _grantee_(self):
        with self._choice():
            with self._option():
                self._token('PUBLIC')
            with self._option():
                self._authorization_identifier_()
            self._error('expecting one of: PUBLIC')

    @graken
    def _assertion_definition_(self):
        self._token('CREATE')
        self._token('ASSERTION')
        self._constraint_name_()
        self._assertion_check_()
        with self._optional():
            self._constraint_attributes_()

    @graken
    def _assertion_check_(self):
        self._token('CHECK')
        self._token('(')
        self._search_condition_()
        self._token(')')

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
            with self._choice():
                with self._option():
                    self._collate_clause_()
                with self._option():
                    self._limited_collation_definition_()
                self._error('no available options')

    @graken
    def _character_set_source_(self):
        self._token('GET')
        self._character_set_name_()

    @graken
    def _limited_collation_definition_(self):
        self._token('COLLATION')
        self._token('FROM')
        self._collation_source_()

    @graken
    def _collation_source_(self):
        with self._choice():
            with self._option():
                self._collating_sequence_definition_()
            with self._option():
                self._translation_collation_()
            self._error('no available options')

    @graken
    def _collating_sequence_definition_(self):
        with self._choice():
            with self._option():
                self._external_collation_()
            with self._option():
                self._schema_collation_name_()
            with self._option():
                self._token('DESC')
                self._token('(')
                self._collation_name_()
                self._token(')')
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT')

    @graken
    def _external_collation_(self):
        self._token('EXTERNAL')
        self._token('(')
        self._token("'")
        self._external_collation_name_()
        self._token("'")
        self._token(')')

    @graken
    def _external_collation_name_(self):
        with self._choice():
            with self._option():
                self._standard_collation_name_()
            with self._option():
                self._implementation_defined_collation_name_()
            self._error('no available options')

    @graken
    def _standard_collation_name_(self):
        self._collation_name_()

    @graken
    def _implementation_defined_collation_name_(self):
        self._collation_name_()

    @graken
    def _schema_collation_name_(self):
        self._collation_name_()

    @graken
    def _translation_collation_(self):
        self._token('TRANSLATION')
        self._translation_name_()
        with self._optional():
            self._token('THEN')
            self._token('COLLATION')
            self._collation_name_()

    @graken
    def _collation_definition_(self):
        self._token('CREATE')
        self._token('COLLATION')
        self._collation_name_()
        self._token('FOR')
        self._character_set_name_()
        self._token('FROM')
        self._collation_source_()
        with self._optional():
            self._pad_attribute_()

    @graken
    def _pad_attribute_(self):
        with self._choice():
            with self._option():
                self._token('NO')
                self._token('PAD')
            with self._option():
                self._token('PAD')
                self._token('SPACE')
            self._error('expecting one of: NO PAD')

    @graken
    def _translation_definition_(self):
        self._token('CREATE')
        self._token('TRANSLATION')
        self._translation_name_()
        self._token('FOR')
        self._character_set_name_()
        self._token('TO')
        self._character_set_name_()
        self._token('FROM')
        self._translation_source_()

    @graken
    def _translation_source_(self):
        self._translation_specification_()

    @graken
    def _translation_specification_(self):
        with self._choice():
            with self._option():
                self._external_translation_()
            with self._option():
                self._token('IDENTITY')
            with self._option():
                self._schema_translation_name_()
            self._error('expecting one of: IDENTITY')

    @graken
    def _external_translation_(self):
        self._token('EXTERNAL')
        self._token('(')
        self._token("'")
        self._external_translation_name_()
        self._token("'")
        self._token(')')

    @graken
    def _external_translation_name_(self):
        with self._choice():
            with self._option():
                self._standard_translation_name_()
            with self._option():
                self._implementation_defined_translation_name_()
            self._error('no available options')

    @graken
    def _standard_translation_name_(self):
        self._translation_name_()

    @graken
    def _implementation_defined_translation_name_(self):
        self._translation_name_()

    @graken
    def _schema_translation_name_(self):
        self._translation_name_()

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
                self._revoke_statement_()
            with self._option():
                self._alter_domain_statement_()
            with self._option():
                self._drop_domain_statement_()
            with self._option():
                self._drop_character_set_statement_()
            with self._option():
                self._drop_collation_statement_()
            with self._option():
                self._drop_translation_statement_()
            with self._option():
                self._drop_assertion_statement_()
            self._error('no available options')

    @graken
    def _drop_schema_statement_(self):
        self._token('DROP')
        self._token('SCHEMA')
        self._schema_name_()
        self._drop_behaviour_()

    @graken
    def _drop_behaviour_(self):
        with self._choice():
            with self._option():
                self._token('CASCADE')
            with self._option():
                self._token('RESTRICT')
            self._error('expecting one of: CASCADE RESTRICT')

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
                self._drop_column_default_clause_()
            self._error('no available options')

    @graken
    def _set_column_default_clause_(self):
        self._token('SET')
        self._default_clause_()

    @graken
    def _drop_column_default_clause_(self):
        self._token('DROP')
        self._token('DEFAULT')

    @graken
    def _drop_column_definition_(self):
        self._token('DROP')
        with self._optional():
            self._token('COLUMN')
        self._column_name_()
        self._drop_behaviour_()

    @graken
    def _add_table_constraint_definition_(self):
        self._token('ADD')
        self._table_constraint_definition_()

    @graken
    def _drop_table_constraint_definition_(self):
        self._token('DROP')
        self._token('CONSTRAINT')
        self._constraint_name_()
        self._drop_behaviour_()

    @graken
    def _drop_table_statement_(self):
        self._token('DROP')
        self._token('TABLE')
        self._table_name_()
        self._drop_behaviour_()

    @graken
    def _drop_view_statement_(self):
        self._token('DROP')
        self._token('VIEW')
        self._table_name_()
        self._drop_behaviour_()

    @graken
    def _revoke_statement_(self):
        self._token('REVOKE')
        with self._optional():
            self._token('GRANT')
            self._token('OPTION')
            self._token('FOR')
        self._privileges_()
        self._token('ON')
        self._object_name_()
        self._token('FROM')

        def sep0():
            self._token(',')

        def block0():
            self._grantee_()

        self._positive_closure(block0, prefix=sep0)
        self._drop_behaviour_()

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
                self._drop_domain_default_clause_()
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
    def _drop_domain_default_clause_(self):
        self._token('DROP')
        self._token('DEFAULT')

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
        self._drop_behaviour_()

    @graken
    def _drop_character_set_statement_(self):
        self._token('DROP')
        self._token('CHARACTER')
        self._token('SET')
        self._character_set_name_()

    @graken
    def _drop_collation_statement_(self):
        self._token('DROP')
        self._token('COLLATION')
        self._collation_name_()

    @graken
    def _drop_translation_statement_(self):
        self._token('DROP')
        self._token('TRANSLATION')
        self._translation_name_()

    @graken
    def _drop_assertion_statement_(self):
        self._token('DROP')
        self._token('ASSERTION')
        self._constraint_name_()

    @graken
    def _simple_value_specification_(self):
        with self._choice():
            with self._option():
                self._parameter_name_()
            with self._option():
                self._literal_()
            self._error('no available options')

    @graken
    def _delete_statement_searched_(self):
        self._token('DELETE')
        self._token('FROM')
        self._table_name_()
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
                with self._optional():
                    self._token('(')
                    self._insert_column_list_()
                    self._token(')')
                self._query_expression_()
            with self._option():
                self._token('DEFAULT')
                self._token('VALUES')
            self._error('expecting one of: DEFAULT')

    @graken
    def _insert_column_list_(self):
        self._column_name_list_()

    @graken
    def _set_clause_list_(self):
        def sep0():
            self._token(',')

        def block0():
            self._set_clause_()

        self._positive_closure(block0, prefix=sep0)

    @graken
    def _set_clause_(self):
        self._object_column_()
        self._token('=')
        self._update_source_()

    @graken
    def _object_column_(self):
        self._column_name_()

    @graken
    def _update_source_(self):
        with self._choice():
            with self._option():
                self._value_expression_()
            with self._option():
                self._token('NULL')
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT NULL')

    @graken
    def _update_statement_searched_(self):
        self._token('UPDATE')
        self._table_name_()
        self._token('SET')
        self._set_clause_list_()
        with self._optional():
            self._token('WHERE')
            self._search_condition_()

    @graken
    def _sql_transaction_statement_(self):
        with self._choice():
            with self._option():
                self._set_transaction_statement_()
            with self._option():
                self._set_constraints_mode_statement_()
            with self._option():
                self._commit_statement_()
            with self._option():
                self._rollback_statement_()
            self._error('no available options')

    @graken
    def _set_transaction_statement_(self):
        self._token('SET')
        self._token('TRANSACTION')

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
    def _diagnostics_size_(self):
        self._token('DIAGNOSTICS')
        self._token('SIZE')
        self._number_of_conditions_()

    @graken
    def _number_of_conditions_(self):
        self._simple_value_specification_()

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
    def _commit_statement_(self):
        self._token('COMMIT')
        with self._optional():
            self._token('WORK')

    @graken
    def _rollback_statement_(self):
        self._token('ROLLBACK')
        with self._optional():
            self._token('WORK')

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
                    self._user_name_()
            with self._option():
                self._token('DEFAULT')
            self._error('expecting one of: DEFAULT')

    @graken
    def _sql_server_name_(self):
        self._simple_value_specification_()

    @graken
    def _connection_name_(self):
        self._simple_value_specification_()

    @graken
    def _user_name_(self):
        self._simple_value_specification_()

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
    def _sql_session_statement_(self):
        with self._choice():
            with self._option():
                self._set_catalog_statement_()
            with self._option():
                self._set_schema_statement_()
            with self._option():
                self._set_names_statement_()
            with self._option():
                self._set_session_authorization_identifier_statement_()
            with self._option():
                self._set_local_time_zone_statement_()
            self._error('no available options')

    @graken
    def _set_catalog_statement_(self):
        self._token('SET')
        self._token('CATALOG')
        self._value_specification_()

    @graken
    def _value_specification_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._general_value_specification_()
            self._error('no available options')

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
    def _set_session_authorization_identifier_statement_(self):
        self._token('SET')
        self._token('SESSION')
        self._token('AUTHORIZATION')
        self._value_specification_()

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
    def _direct_sql_statement_(self):
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
                self._temporary_table_declaration_()
            self._error('no available options')

    @graken
    def _direct_select_statement_multiple_rows_(self):
        self._query_expression_()
        with self._optional():
            self._order_by_clause_()
