# -*- coding:utf-8 -*-
# author: lkz
# date: 2015/10/15 17:14

from flask import Blueprint, url_for, g, request


test_bp = Blueprint('test', __name__, subdomain='<subdomain>')


@test_bp.route('/')
def test_arrival(subdomain):
    return "<h2 style='color:red'>%s</h2>" %  request.url


@test_bp.route('/index')
def test_sub_domain(subdomain):
    return "success"
