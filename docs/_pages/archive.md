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
{% include record-card.html record=r search=true %}
{% endfor %}
</div>

<p class="no-results" id="no-results" hidden>No records match your search. <button type="button" id="clear-filters-2" class="clear-filters">Clear filters</button></p>

<script src="{{ '/assets/js/archive-search.js' | relative_url }}"></script>
