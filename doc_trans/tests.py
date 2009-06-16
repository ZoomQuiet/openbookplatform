# -*- coding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from doc_trans.models import *
import time
#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.failUnlessEqual(1 + 1, 2)
#
#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.
#
#>>> 1 + 1 == 2
#True
#"""}

class TranslationTest(TestCase):
    def setUp(self):
        project = Project.objects.create(name='test_submit_translation', )
        version = Version.objects.create(project = project, revision='1', )
        test_page = Page.objects.create(project = project, path='test_page_path', current_version = version)
        test_paragraph = Paragraph.objects.create(page = test_page, original='test_paragraph_original', current_version = version, ordinal = 1)
        test_user = User.objects.create(username = 'test_user')
        
        
    def test_submit_translation(self):
        test_paragraph = Paragraph.objects.get(original='test_paragraph_original')
        test_user = User.objects.get(username = 'test_user')
        new_translation = Translation(paragraph = test_paragraph, history_translation = test_paragraph.latest_translation,
                                          translator = test_user, content = u"测试翻译提交", ip = '')
    
    def test_modify_translation(self):
        test_paragraph = Paragraph.objects.get(original='test_paragraph_original')
        test_user = User.objects.get(username = 'test_user')
        first_translation = Translation(paragraph = test_paragraph, history_translation = test_paragraph.latest_translation,
                                          translator = test_user, content = u"第一个翻译", ip = '')
        first_translation.save()
        test_paragraph = Paragraph.objects.get(original='test_paragraph_original')
        self.assertEqual(first_translation, test_paragraph.latest_translation)
        
        
        time.sleep(1)
        second_translation = Translation(paragraph = test_paragraph, history_translation = test_paragraph.latest_translation,
                                          translator = test_user, content = u"第二个翻译", ip = '')
        second_translation.save()
        test_paragraph = Paragraph.objects.get(original='test_paragraph_original')
        self.assertEqual(second_translation, test_paragraph.latest_translation)
        self.assertEqual(first_translation, second_translation.history_translation)
        
    