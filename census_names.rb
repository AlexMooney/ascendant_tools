# frozen_string_literal: true

require 'csv'
require 'pry'

class CensusNames
  attr_reader :count_by_surname, :surname_row_by_surname

  def initialize
    @surname_rows = CSV.read('data/surnames01.csv', headers: true)
    @surname_row_by_surname = @surname_rows.each_with_object({}) do |surname_row, result|
      result[surname_row['Name']] = clean_row!(surname_row)
    end
    @count_by_surname = @surname_row_by_surname.transform_values { |row| row['Count'] }
  end

  def random_person
    surname = random_surname
    surname_row = surname_row_by_surname[surname]
    ethnicity = random_ethnicity(surname_row)
    "#{surname} #{ethnicity}"
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

puts CensusNames.new.random_person
