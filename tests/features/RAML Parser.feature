# Created by mpetyx at 1/16/15
Feature: parse raml files
  pyapi should be able to parse raml file documents according to the 0.8 version

  Scenario: parse documentation
    Given A raml document
    When i parse it
    Then I should print the documentation