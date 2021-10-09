# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name = "best_movies"

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://ken:ken569972@cluster0-ahixq.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client['IMDB']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLlitePipeline(object):

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title,year,duration,genre,rating,movie_url) VALUES(?,?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('movie_url')
        ))
        self.connection.commit()
        return item