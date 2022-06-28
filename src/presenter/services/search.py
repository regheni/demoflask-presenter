from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename

import os
import ipdb
import json

from presenter.models.movie import Movie
from presenter.models.actor import Actor


class SearchItem:
    def __init__(self):
        pass

    def search(self, query=""):
        results = dict()
        for model, attribute in self._searchable_model():
            results[model.__tablename__] = self._model_search(model, attribute, query)
        return results

    def _searchable_model(self):
        return [(Movie, "title"), (Actor, "name")]

    def _model_search(self, model, attribute, query):
        return model.query.filter(getattr(model, attribute).like("%" + query + "%")).all()
