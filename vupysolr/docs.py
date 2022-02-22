"""
Parse Solr stored VuFind records.

For the Solr schema used by VuFind, see
https://vufind.org/wiki/development:architecture:solr_index_schema

For the XML schema used by Solr, see
https://github.com/vufind-org/vufind/blob/dev/solr/vufind/biblio/conf/schema.xml
"""

import datetime
import dateutil.parser

DT005 = "%Y%m%d%H%M%S.0"


class VuFindParser:

    def __init__(self, doc, marc=False):
        self.raw = doc
        self.fields = self._names()
        self.marc = None
        if marc:
            self.marc = VuFindMarcParser(doc)

    def _names(self):
        if self.raw:
            names = list(self.raw.keys())
            names.sort()
            return names
        return []

    def _field(self, name):
        if self.raw and name in self.raw:
            return self.raw[name]

    def _field_first(self, name):
        field_list = self._field(name)
        if field_list and len(field_list) > 0:
            return field_list[0]

    def _field_joined(self, name, delim="|"):
        field_list = self._field(name)
        if field_list and len(field_list) > 0:
            return delim.join(field_list)

    def get(self, name):
        return self._field(name)

    # static fields

    @property
    def _version_(self):
        return self._field("_version_")

    @property
    def author(self):
        return self._field("author")

    @property
    def building(self):
        return self._field("building")

    @property
    def container_title(self):
        return self._field("container_title")

    @property
    def ctrlnum(self):
        return self._field("ctrlnum")

    @property
    def edition(self):
        return self._field("edition")

    @property
    def first_indexed(self):
        return self._field("first_indexed")

    @property
    def first_indexed_datetime(self):
        timestamp = self.last_indexed
        if timestamp:
            return dateutil.parser.isoparse(timestamp)

    @property
    def format(self):
        return self._field("format")

    @property
    def fullrecord(self):
        return self._field("fullrecord")

    @property
    def hierarchytype(self):
        return self._field("hierarchytype")

    @property
    def hierarchy_top_id(self):
        return self._field("hierarchy_top_id")

    @property
    def hierarchy_parent_id(self):
        return self._field("hierarchy_top_id")

    @property
    def id(self):
        return self._field("id")

    @property
    def institution(self):
        return self._field("institution")

    @property
    def is_hierarchy_id(self):
        return self._field("is_hierarchy_id")

    @property
    def isbn(self):
        return self._field("isbn")

    @property
    def issn(self):
        return self._field("issn")

    @property
    def language(self):
        return self._field("language")

    @property
    def last_indexed(self):
        return self._field("last_indexed")

    @property
    def last_indexed_datetime(self):
        timestamp = self.last_indexed
        if timestamp:
            return dateutil.parser.isoparse(timestamp)

    @property
    def marc_error(self):
        return self._field("marc_error")

    @property
    def publish_date(self):
        return self._field("publishDate")

    @property
    def publish_date_sort(self):
        return self._field("publishDateSort")

    @property
    def publisher(self):
        return self._field("publisher")

    @property
    def record_format(self):
        return self._field("record_format")

    @property
    def recordtype(self):
        return self._field("recordtype")    # depracted 6.0 / removed 7.0

    @property
    def title(self):
        return self._field("title")

    @property
    def title_short(self):
        return self._field("title_short")

    @property
    def thumbnail(self):
        return self._field("thumbnail")

    @property
    def url(self):
        return self._field("url")

    # dynamic fields

    @property
    def doi_str_mv(self):
        return self._field("doi_str_mv")

    # marc fields

    @property
    def marc_latest_transaction(self):
        if self.marc is not None:
            return self.marc.latest_transaction

    @property
    def marc_latest_transaction_datetime(self):
        if self.marc is not None:
            return self.marc.latest_transaction_datetime

    @property
    def marc_latest_transaction_iso(self):
        if self.marc is not None:
            return self.marc.latest_transaction_iso

    @property
    def marc_date_entered(self):
        if self.marc is not None:
            return self.marc.date_entered

    @property
    def marc_date_entered_date(self):
        if self.marc is not None:
            return self.marc.date_entered_date

    @property
    def marc_date_entered_iso(self):
        if self.marc is not None:
            return self.marc.date_entered_iso


class VuFindMarcParser:

    def __init__(self, doc):
        self.fullrecord = None
        if "fullrecord" in doc:
            self.fullrecord = doc["fullrecord"]

    @property
    def fields(self):
        if self.fullrecord is not None and type(self.fullrecord) == dict:
            if "fields" in self.fullrecord:
                return self.fullrecord["fields"]

    @property
    def latest_transaction(self):
        if self.fields is not None:
            for field in self.fields:
                if "005" in field:
                    return field["005"]

    @property
    def latest_transaction_datetime(self):
        latest_trans = self.latest_transaction
        if latest_trans is not None:
            try:
                return datetime.datetime.strptime(latest_trans, DT005)
            except ValueError:
                pass

    @property
    def latest_transaction_iso(self):
        latest_trans_datetime = self.latest_transaction_datetime
        if latest_trans_datetime is not None:
            return latest_trans_datetime.isoformat()

    @property
    def date_entered(self):
        if self.fields is not None:
            for field in self.fields:
                if "008" in field:
                    return field["008"][:6]

    @property
    def date_entered_date(self):
        date_entered = self.date_entered
        if date_entered is not None and len(date_entered.strip()) == 6:
            try:
                return datetime.datetime.strptime(date_entered, "%y%m%d").date()
            except ValueError:
                pass

    @property
    def date_entered_iso(self):
        date_entered_date = self.date_entered_date
        if date_entered_date is not None:
            return date_entered_date.isoformat()
