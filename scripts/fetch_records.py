#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# fetch_records.py
# The Lighting Design Archive — LD-Archive.org
# Author: Anthony Arblaster
#
# Pulls records from a Humanities Commons (Knowledge Commons Works)
# community and writes them, normalised, to docs/_data/records.json so the
# static site can render and search them.
#
# The site never talks to the API at page-load time: this runs at build
# time (see .github/workflows/fetch-records.yml) and the site reads the
# cached JSON.
#
# KC Works runs InvenioRDM. Two instance-specific facts verified against the
# live API (2026-07), NOT assumed:
#   * Community records come from  /api/communities/<slug>/records
#     The Zenodo-style  /api/records?communities=<slug>  is SILENTLY IGNORED
#     by KC Works and returns the entire 42k-record repository.
#   * access.record is "public" / "restricted" (not Zenodo's "open").
#   * custom fields use a "kcr:" prefix; there are no arbitrary per-community
#     fields, so domain metadata (venue, director, company) has no native home
#     yet — see the note in normalise_record().
#
# Dependency-free (standard library only).
#
# Usage:
#   python3 scripts/fetch_records.py \
#       --base-url https://works.hcommons.org \
#       --community lighting-design-archive \
#       --out docs/_data/records.json
# ---------------------------------------------------------------------------

import argparse
import json
import sys
import urllib.parse
import urllib.request

PAGE_SIZE = 100
USER_AGENT = "ld-archive-web/1.0 (+https://ld-archive.org)"
SOURCE_NAME = "Humanities Commons"


def fetch_page(base_url, community, page):
	"""Fetch one page of a community's records from the KC Works API."""
	query = urllib.parse.urlencode({"size": PAGE_SIZE, "page": page})
	url = "{}/api/communities/{}/records?{}".format(
		base_url.rstrip("/"), urllib.parse.quote(community), query
	)
	request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
	with urllib.request.urlopen(request, timeout=30) as response:
		return json.loads(response.read().decode("utf-8"))


def year_from_date(date_string):
	"""Extract a 4-digit year from an ISO-ish date string."""
	if isinstance(date_string, str) and len(date_string) >= 4:
		return date_string[:4]
	return ""


def resource_type_title(metadata):
	"""Human-readable resource type, e.g. 'Report'."""
	resource_type = metadata.get("resource_type")
	if isinstance(resource_type, dict):
		return resource_type.get("title", {}).get("en", "")
	return ""


def collect_keywords(metadata, custom):
	"""Merge FAST/topical subjects with the depositor's free-text tags."""
	keywords = [
		subject.get("subject", "") if isinstance(subject, dict) else str(subject)
		for subject in metadata.get("subjects", [])
	]
	keywords += custom.get("kcr:user_defined_tags", []) or []
	return [k for k in keywords if k]


def normalise_record(hit):
	"""Map one KC Works record onto the archive's flat record shape.

	Standard fields (title, creators->designers, date, DOI, access, keywords)
	map cleanly. Domain-specific fields (venue, company, director) have no
	native home on Humanities Commons: KC Works exposes only fixed "kcr:"
	custom fields, not arbitrary per-community ones. Until a metadata
	convention is agreed (likely encoding them in kcr:user_defined_tags, e.g.
	"venue:The Old Vic"), these are left blank rather than guessed.
	"""
	metadata = hit.get("metadata", {})
	custom = hit.get("custom_fields", {})

	designers = [
		creator.get("person_or_org", {}).get("name") or creator.get("name", "")
		for creator in metadata.get("creators", [])
	]
	designers = [name for name in designers if name]

	doi = hit.get("pids", {}).get("doi", {}).get("identifier", "")
	doi_url = (
		"https://doi.org/" + doi
		if doi
		else hit.get("links", {}).get("self_html", "")
	)

	files = [
		{"name": name, "size": entry.get("size", "")}
		for name, entry in (hit.get("files", {}).get("entries", {}) or {}).items()
	]

	return {
		"id": str(hit.get("id", "")),
		"title": metadata.get("title", "Untitled"),
		"designers": designers,
		"company": "",   # no native field on HC — see docstring
		"venue": "",     # no native field on HC — see docstring
		"director": "",  # no native field on HC — see docstring
		"year": year_from_date(metadata.get("publication_date", "")),
		"doi": doi,
		"doi_url": doi_url,
		"source": SOURCE_NAME,
		"access": hit.get("access", {}).get("record", ""),
		"resource_type": resource_type_title(metadata),
		"description": metadata.get("description", ""),
		"keywords": collect_keywords(metadata, custom),
		"files": files,
	}


def fetch_all(base_url, community):
	"""Page through the community and return all normalised records."""
	records = []
	page = 1
	while True:
		payload = fetch_page(base_url, community, page)
		hits = payload.get("hits", {}).get("hits", [])
		if not hits:
			break
		records.extend(normalise_record(hit) for hit in hits)
		total = payload.get("hits", {}).get("total", 0)
		if len(records) >= total or len(hits) < PAGE_SIZE:
			break
		page += 1
	return records


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--base-url", default="https://works.hcommons.org")
	parser.add_argument("--community", default="lighting-design-archive")
	parser.add_argument("--out", default="docs/_data/records.json")
	args = parser.parse_args()

	try:
		records = fetch_all(args.base_url, args.community)
	except Exception as error:  # noqa: BLE001 — fail loudly in CI
		print("Failed to fetch records: {}".format(error), file=sys.stderr)
		return 1

	with open(args.out, "w", encoding="utf-8") as handle:
		json.dump(records, handle, indent=2, ensure_ascii=False)
		handle.write("\n")

	print("Wrote {} records to {}".format(len(records), args.out))
	return 0


if __name__ == "__main__":
	sys.exit(main())
