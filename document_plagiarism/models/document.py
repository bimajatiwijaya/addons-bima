# -*- coding: utf-8 -*-
from odoo import models, fields, api
from . import cosineSim


class Document(models.Model):
    _name = 'document.document'

    name = fields.Char("Name")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], string='State', required=True, default='draft')
    description = fields.Text("Description")
    document_ids = fields.One2many('document.plagiarism', 'document_id')
    plagiarism_average = fields.Float(compute='_average_plagiarism')

    def _average_plagiarism(self):
        """
        This method will calculate average similarity from all compared documents
        :return:
        """
        for doc in self:
            total = 0.0
            for line in doc.document_ids:
                total += line.cosine_similarity
            total_checked = len(doc.document_ids)
            if total_checked > 0:
                doc.plagiarism_average = total / total_checked

    def check_cosine_sim(self):
        """
        This method will compare the active document with confirmed document
        and record similarity threshold
        :return:
        """
        self.ensure_one()
        all_docs = self.search([('state', '=', 'confirm')])
        doc_ids = self.document_ids
        for doc in all_docs:
            similarity_result = cosineSim.cosineSim(
                doc.description, self.description)
            exist = doc_ids.filtered(lambda a: a.compared_document_id.id != self.id)
            if exist:
                for lin_doc in exist:
                    if lin_doc.cosine_similarity != similarity_result:
                        lin_doc.write({'cosine_similarity': similarity_result})
                    else:
                        continue
            else:
                if self.id != doc.id:
                    self.env['document.plagiarism'].create(
                        {'document_id': self.id,
                         'cosine_similarity': similarity_result,
                         'compared_document_id': doc.id})

    @api.multi
    def confirm(self):
        self.write({'state': 'confirm'})


class DocumentAnalysis(models.Model):
    _name = 'document.plagiarism'

    document_id = fields.Many2one('document.document')
    compared_document_id = fields.Many2one('document.document')
    cosine_similarity = fields.Float('Cosine similarity')

    _sql_constraints = [
        ('document_id_uniq', 'unique(document_id, compared_document_id)', 'Document should be unique'),
    ]

