local dependency_added = false

local function stringify(value)
  if value == nil then
    return nil
  end
  return pandoc.utils.stringify(value)
end

local function escape_html(value)
  return value:gsub("&", "&amp;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;")
    :gsub('"', "&quot;")
    :gsub("'", "&#39;")
end

return {
  ["obsidian-canvas"] = function(args, kwargs)
    local path = stringify(kwargs.path or args[1])
    if path == nil or path == "" then
      return pandoc.RawBlock(
        "html",
        '<div class="ocq-error" role="alert">Obsidian Canvas: the <code>path</code> attribute is required.</div>'
      )
    end

    local height = stringify(kwargs.height) or "75vh"
    local initial_view = stringify(kwargs["initial-view"]) or "fit"
    local controls = stringify(kwargs.controls) or "true"
    local previews = stringify(kwargs.previews) or "true"
    if initial_view ~= "fit" and initial_view ~= "reset" then
      error("obsidian-canvas initial-view must be 'fit' or 'reset'")
    end
    if controls ~= "true" and controls ~= "false" then
      error("obsidian-canvas controls must be 'true' or 'false'")
    end
    if previews ~= "true" and previews ~= "false" then
      error("obsidian-canvas previews must be 'true' or 'false'")
    end
    if not height:match("^[%w%s%%%(%)%+%-%*%./]+$") then
      error("obsidian-canvas height contains unsupported characters")
    end

    if not dependency_added then
      quarto.doc.add_html_dependency({
        name = "obsidian-canvas",
        version = "0.3.0",
        scripts = {"obsidian-canvas.js"},
        stylesheets = {"obsidian-canvas.css"}
      })
      dependency_added = true
    end

    local html = string.format([[
<div class="ocq-canvas" tabindex="0" role="region" aria-label="Interactive read-only canvas" data-ocq-path="%s" data-ocq-initial-view="%s" data-ocq-controls="%s" data-ocq-previews="%s" style="--ocq-height:%s">
  <div class="ocq-loading" role="status">Preparing canvas&hellip;</div>
  <noscript><p class="ocq-fallback">JavaScript is required for the spatial canvas. <a href="%s">Open the linear canvas content</a>.</p></noscript>
</div>]], escape_html(path), initial_view, controls, previews, escape_html(height), escape_html(path:gsub("%.json$", "-fallback.html")))
    local math_loader = pandoc.Div(
      {pandoc.Para({pandoc.Math("InlineMath", "0")})},
      pandoc.Attr("", {"ocq-math-loader"}, {{"aria-hidden", "true"}})
    )
    return pandoc.Blocks({pandoc.RawBlock("html", html), math_loader})
  end
}
