# Pantry Inventory

## Contributing:

William Barnett, Elena Hernandez, and Anthony Rodriguez-Miranda


## Table of Contents
- [Introduction](#introduction)
- [Usage](#usage)
- [Languages Used](#languages-used)
- [Frameworks and Libraries](#frameworks-and-libraries)
- [Code Explanations](#code-explanations)

## Introduction

In this project we used the Spoonacular API to post and request data to find recipe recommendations based on items recorded in a list.

## Usage

This tool can generate a list of recipes based on data recorded in a list. Users create this list by entering the items, amount of each item, and price of each item.


## Languages Used:

- **Python**: The main programming language used for backend development and interacting with the Spoonacular API.
- **HTML**: A markup language used for structuring the web pages and forms.
- **CSS**:  Used for styling the web pages and improving the visual appearance.

## Frameworks and Libraries

- **Flask**: A lightweight WSGI web application framework used to build the web application and handle routing.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python, used to interact with the database.

## Code Explanations

The code in the tests folders holds unit tests that check if the database model and webpages functions. Those tests and the style checks have been automated with the files in the .github/workflows folders. The project folder holds the templates for the webpage. This folder also holds a file that creates the database model that holds the inventory list, a file that creates the routes to the different webpages, and a file that calls the Spoonacular API.