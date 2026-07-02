<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
  xmlns:html="http://www.w3.org/TR/REC-html40"
  xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>XML Sitemap — GstarCADemy</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <style type="text/css">
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
      color: #333;
      margin: 0;
      padding: 0;
    }
    #content {
      max-width: 980px;
      margin: 0 auto;
      padding: 30px 20px;
    }
    h1 {
      font-size: 28px;
      font-weight: 700;
      margin: 0 0 10px;
    }
    p.desc {
      font-size: 14px;
      color: #666;
      margin: 0 0 6px;
    }
    p.desc a {
      color: #c0392b;
      text-decoration: none;
    }
    p.desc a:hover {
      text-decoration: underline;
    }
    p.count {
      font-size: 13px;
      color: #555;
      margin: 20px 0 12px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      border-spacing: 0;
      font-size: 13px;
    }
    th {
      text-align: left;
      padding: 10px 8px;
      border-bottom: 1px solid #ccc;
      background: #f7f7f7;
      font-weight: 600;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    td {
      padding: 8px;
      border-bottom: 1px solid #eee;
    }
    tr:hover td {
      background: #f9f9f9;
    }
    td a {
      color: #1a0dab;
      text-decoration: none;
    }
    td a:hover {
      text-decoration: underline;
    }
    .lastmod {
      white-space: nowrap;
      color: #555;
    }
    #footer {
      margin-top: 30px;
      padding-top: 14px;
      border-top: 1px solid #eee;
      font-size: 12px;
      color: #999;
    }
  </style>
</head>
<body>
<div id="content">
  <h1>XML Sitemap</h1>
  <p class="desc">This is an XML Sitemap, meant for consumption by search engines.</p>
  <p class="desc">You can find more information about XML sitemaps on <a href="https://www.sitemaps.org/" target="_blank">sitemaps.org</a>.</p>

  <xsl:if test="sitemap:urlset">
    <p class="count">This XML Sitemap contains <strong><xsl:value-of select="count(sitemap:urlset/sitemap:url)"/></strong> URLs.</p>
    <table>
      <thead>
        <tr>
          <th style="width:80%">URL</th>
          <th style="width:20%">Last Modified</th>
        </tr>
      </thead>
      <tbody>
        <xsl:for-each select="sitemap:urlset/sitemap:url">
          <tr>
            <td>
              <a href="{sitemap:loc}"><xsl:value-of select="sitemap:loc"/></a>
            </td>
            <td class="lastmod">
              <xsl:value-of select="sitemap:lastmod"/>
            </td>
          </tr>
        </xsl:for-each>
      </tbody>
    </table>
  </xsl:if>

  <xsl:if test="sitemap:sitemapindex">
    <p class="count">This XML Sitemap Index contains <strong><xsl:value-of select="count(sitemap:sitemapindex/sitemap:sitemap)"/></strong> sitemaps.</p>
    <table>
      <thead>
        <tr>
          <th style="width:80%">Sitemap</th>
          <th style="width:20%">Last Modified</th>
        </tr>
      </thead>
      <tbody>
        <xsl:for-each select="sitemap:sitemapindex/sitemap:sitemap">
          <tr>
            <td>
              <a href="{sitemap:loc}"><xsl:value-of select="sitemap:loc"/></a>
            </td>
            <td class="lastmod">
              <xsl:value-of select="sitemap:lastmod"/></td>
          </tr>
        </xsl:for-each>
      </tbody>
    </table>
  </xsl:if>

  <div id="footer">
    Generated for <a href="https://gstarcademy.com/" style="color:#999;">GstarCADemy</a>
  </div>
</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
