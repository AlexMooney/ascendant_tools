#!/usr/bin/env ruby
# frozen_string_literal: true

require 'csv'
require 'pry'

class CensusNames
  attr_reader :count_by_surname, :surname_row_by_surname

  def initialize
    surname_rows = CSV.read('data/surnames_01.csv', headers: true)
    @surname_row_by_surname = surname_rows.each_with_object({}) do |surname_row, result|
      result[surname_row['Name']] = clean_row!(surname_row)
    end
    @count_by_surname = @surname_row_by_surname.transform_values { |row| row['Count'] }

    male_name_rows = CSV.read('data/male_names_01.csv', headers: true)
    @count_by_male_name = male_name_rows.each_with_object({}) do |male_name_row, result|
      result[male_name_row['Name']] = male_name_row['Count'].gsub(',', '').to_i
    end

    female_name_rows = CSV.read('data/female_names_01.csv', headers: true)
    @count_by_female_name = female_name_rows.each_with_object({}) do |female_name_row, result|
      result[female_name_row['Name']] = female_name_row['Count'].gsub(',', '').to_i
    end
  end

  def random_person
    firstname = picker([@count_by_male_name, @count_by_female_name].sample)
    surname = random_surname
    surname_row = surname_row_by_surname[surname]
    ethnicity = random_ethnicity(surname_row)
    "#{firstname} #{surname}, #{ethnicity}"
  end

  def random_surname
    picker(count_by_surname)
  end

  def random_ethnicity(surname_row)
    count_by_ethnicity = {
      'White' => surname_row['White'],
      'Black' => surname_row['Black'],
      'Hispanic' => surname_row['Hispanic'],
      'Asian & Pacific Islander' => surname_row['API'],
      'American Indian' => surname_row['AIAN'],
      'Two or More' => surname_row['Two or More']
    }
    picker(count_by_ethnicity)
  end

  private

  def picker(count_by_label)
    current = 0
    max = count_by_label.values.inject(:+)
    random_value = rand(max) + 1
    count_by_label.each do |label, count|
      current += count
      return label if random_value <= current
    end
  end

  def clean_row!(row)
    row['Count'] = row['Count'].gsub(',', '').to_i

    ['White', 'Black', 'Hispanic', 'API', 'AIAN', 'Two or More'].each do |ethnicity|
      row[ethnicity] = csv_float_to_count(row, ethnicity)
    end

    row
  end

  def csv_float_to_count(row, key)
    (row[key].to_f * 100).to_i
  end
end

census_names = CensusNames.new
10.times { puts census_names.random_person }
