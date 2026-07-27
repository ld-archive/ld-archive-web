---
layout: single
title: "Archive"
permalink: /archive/
classes: wide
author_profile: false
---

<link rel="stylesheet" href="{{ '/assets/css/archive.css' | relative_url }}">

<p class="archive-intro">Browse lighting design materials contributed by lighting designers. Every record links out to its permanent, citable record (with a DOI) on the archive backend.</p>

<p class="sample-banner">⚠️ <strong>Sample data.</strong> These {{ site.data.records | size }} records are placeholders to demonstrate the browse-and-search experience. Real records will be pulled in automatically once the archive community exists.</p>

<div class="archive-controls" id="archive-controls" hidden>
  <input type="search" id="archive-search-input" class="archive-search"
    placeholder="Search productions, designers, venues, keywords…"
    aria-label="Search the archive" autocomplete="off">
  <div class="archive-facets">
    <label>Designer
      <select id="facet-designer"><option value="">All</option></select>
    </label>
    <label>Venue
      <select id="facet-venue"><option value="">All</option></select>
    </label>
    <label>Year
      <select id="facet-year"><option value="">All</option></select>
    </label>
    <button type="button" id="clear-filters" class="clear-filters">Clear</button>
  </div>
</div>

<p class="result-count" id="result-count" aria-live="polite"></p>

<div class="records-grid" id="records">
{% for r in site.data.records %}
  {% assign designers = r.designers | join: "||" %}
  {% capture blob %}{{ r.title }} {{ r.designers | join: " " }} {{ r.venue }} {{ r.director }} {{ r.company }} {{ r.description }} {{ r.keywords | join: " " }} {{ r.year }}{% endcapture %}
  <article class="record-card"
    data-search="{{ blob | strip_newlines | downcase | escape }}"
    data-designers="{{ designers | downcase | escape }}"
    data-designers-display="{{ r.designers | join: '||' | escape }}"
    data-venue="{{ r.venue | escape }}"
    data-year="{{ r.year }}">
    <h3 class="record-title">{{ r.title }}</h3>
    {% if r.designers %}<p class="record-designers">{{ r.designers | join: ", " }}</p>{% endif %}
    <ul class="record-meta">
      {% if r.venue %}<li><span class="k">Venue</span> {{ r.venue }}</li>{% endif %}
      {% if r.company %}<li><span class="k">Company</span> {{ r.company }}</li>{% endif %}
      {% if r.director %}<li><span class="k">Director</span> {{ r.director }}</li>{% endif %}
      {% if r.year %}<li><span class="k">Year</span> {{ r.year }}</li>{% endif %}
    </ul>
    {% if r.description %}<p class="record-desc">{{ r.description | strip_html | truncate: 180 }}</p>{% endif %}
    {% if r.keywords %}<p class="record-keywords">{% for k in r.keywords %}<span class="tag">{{ k }}</span>{% endfor %}</p>{% endif %}
    <p class="record-links">
      {% if r.doi_url %}<a href="{{ r.doi_url }}" rel="noopener" class="record-doi">View record on {{ r.source | default: "Humanities Commons" }} &rarr;</a>{% endif %}
      {% if r.access %}<span class="access access-{{ r.access }}">{{ r.access }} access</span>{% endif %}
    </p>
  </article>
{% endfor %}
</div>

<p class="no-results" id="no-results" hidden>No records match your search. <button type="button" id="clear-filters-2" class="clear-filters">Clear filters</button></p>

<script src="{{ '/assets/js/archive-search.js' | relative_url }}"></script>
