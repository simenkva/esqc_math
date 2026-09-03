---@meta

---@class CustomCalloutDefinition
---@field type string The type/identifier of the callout
---@field title string|pandoc.Inlines|nil The title of the callout
---@field icon boolean|nil Whether to show an icon
---@field appearance string|nil The appearance style ('default', 'minimal', 'simple')
---@field collapse boolean|string|nil Whether the callout is collapsible
---@field icon_symbol string|nil Custom icon symbol or font awesome icon
---@field html_icon_png string|nil Path to a PNG icon for HTML outputs
---@field html_icon_svg string|nil Path to an SVG icon for HTML outputs
---@field epub_icon_png string|nil Path to a PNG icon for EPUB outputs
---@field color string|nil The color of the callout
---@field background_color string|nil The background color of the callout

---@class CustomCalloutsMap

-- Global variable to store custom callout definitions
---@type table<string, CustomCalloutDefinition>
local customCallouts = {}
local epubGeneratedCssFile = nil

local fa = require("fa")

---Checks whether the current output format is EPUB
---@return boolean
local function isEpubOutput()
  if quarto ~= nil and quarto.doc ~= nil and quarto.doc.is_format ~= nil and quarto.doc.is_format("epub") then
    return true
  end
  if FORMAT ~= nil and string.match(FORMAT, "^epub") then
    return true
  end
  return _quarto ~= nil and
    _quarto.format ~= nil and
    _quarto.format.isEpubOutput ~= nil and
    _quarto.format.isEpubOutput()
end

---Checks whether Font Awesome webfont icons can be used
---@return boolean
local function canUseFontAwesome()
  if isEpubOutput() then
    return false
  end
  if quarto ~= nil and quarto.doc ~= nil and quarto.doc.is_format ~= nil then
    return quarto.doc.is_format("html:js") or quarto.doc.is_format("html") or quarto.doc.is_format("revealjs")
  end
  if FORMAT ~= nil then
    return string.match(FORMAT, "html") ~= nil or string.match(FORMAT, "revealjs") ~= nil
  end
  return _quarto ~= nil and
    _quarto.format ~= nil and
    _quarto.format.isHtmlOutput ~= nil and
    _quarto.format.isHtmlOutput()
end

---Resolves a temporary CSS path for EPUB custom callout styles
---@return string
local function resolveEpubCssFile()
  if epubGeneratedCssFile == nil then
    epubGeneratedCssFile = os.tmpname()
    if not string.match(epubGeneratedCssFile, "%.css$") then
      epubGeneratedCssFile = epubGeneratedCssFile .. ".css"
    end
  end
  return epubGeneratedCssFile
end

---Writes generated CSS for EPUB and appends it to the document's CSS metadata
---@param meta pandoc.Meta The document metadata
---@param css string The generated CSS rules
local function attachEpubCss(meta, css)
  local cssFilePath = resolveEpubCssFile()
  local file = io.open(cssFilePath, "w")
  if file == nil then
    return
  end
  file:write(css)
  file:close()

  local cssMeta = meta["css"]
  if cssMeta == nil then
    meta["css"] = pandoc.MetaList({ pandoc.MetaString(cssFilePath) })
  elseif cssMeta.t == "MetaList" then
    for _, item in ipairs(cssMeta) do
      if pandoc.utils.stringify(item) == cssFilePath then
        return
      end
    end
    cssMeta:insert(pandoc.MetaString(cssFilePath))
    meta["css"] = cssMeta
  elseif pandoc.utils.stringify(cssMeta) ~= cssFilePath then
    meta["css"] = pandoc.MetaList({ cssMeta, pandoc.MetaString(cssFilePath) })
  end
end

---Converts a valid CSS color string or hexadecimal to RGBA format
---@param color string The color in hex (#RRGGBB) or named format
---@param alpha number The alpha value between 0 and 1
---@return string rgba The color in rgba() or rgb(from color) format
local function colorToRgba(color, alpha)
  if color:sub(1,1) == "#" then
    local r = tonumber(color:sub(2,3), 16)
    local g = tonumber(color:sub(4,5), 16)
    local b = tonumber(color:sub(6,7), 16)
    return string.format("rgba(%d, %d, %d, %.2f)", r, g, b, alpha)
  else
    -- For named colors, we use the functional notation of rgba()
    return string.format("rgb(from %s r g b / %.0f%%)", color, alpha * 100)
  end
end

---CSS named color to hex lookup (without #, uppercase)
---@type table<string, string>
local cssNamedColors = {
  -- CSS Level 1
  black = "000000", silver = "C0C0C0", gray = "808080", white = "FFFFFF",
  maroon = "800000", red = "FF0000", purple = "800080", fuchsia = "FF00FF",
  green = "008000", lime = "00FF00", olive = "808000", yellow = "FFFF00",
  navy = "000080", blue = "0000FF", teal = "008080", aqua = "00FFFF",
  -- Extended common colors
  orange = "FFA500", pink = "FFC0CB", brown = "A52A2A",
  cyan = "00FFFF", grey = "808080",
  crimson = "DC143C", coral = "FF7F50", gold = "FFD700",
  indigo = "4B0082", violet = "EE82EE",
  steelblue = "4682B4", dodgerblue = "1E90FF",
  forestgreen = "228B22", tomato = "FF6347",
  darkorange = "FF8C00", firebrick = "B22222",
  slategray = "708090", darkred = "8B0000",
}

---Converts a color string to a 6-digit uppercase hex value (without #)
---@param color string The color in hex (#RRGGBB) or named CSS format
---@return string|nil hex The 6-digit hex string, or nil if conversion fails
local function colorToHex(color)
  if color:sub(1, 1) == "#" then
    return color:sub(2):upper()
  end
  return cssNamedColors[color:lower()]
end

---Adds HTML dependency for bundled FontAwesome 7 Free Solid font
local function ensureFontAwesomeDeps()
  quarto.doc.add_html_dependency({
    name = "fontawesome-7-free",
    version = "7.2.0",
    stylesheets = {"assets/css/fontawesome.css"},
    resources = {
      { name = "fa-solid-900.woff2", path = "assets/webfonts/fa-solid-900.woff2" }
    }
  })
end

---Checks if a string represents a Font Awesome icon
---@param icon string|nil The icon string to check
---@return boolean is_fa True if the string starts with "fa-"
local function isFontAwesomeIcon(icon)
  return icon ~= nil and icon:sub(1, 3) == "fa-"
end

---Converts a metadata value to a non-empty string
---@param value any
---@return string|nil
local function metaValueToString(value)
  if value == nil then
    return nil
  end
  local text = pandoc.utils.stringify(value)
  return text ~= "" and text or nil
end

---Returns a nested metadata value by path segments
---@param value any
---@param path string[]
---@return any
local function metaLookupPath(value, path)
  local current = value
  for _, key in ipairs(path) do
    if type(current) ~= "table" then
      return nil
    end
    current = current[key]
    if current == nil then
      return nil
    end
  end
  return current
end

---Returns the first non-nil value
---@param ... any
---@return any
local function firstNonNil(...)
  for i = 1, select("#", ...) do
    local value = select(i, ...)
    if value ~= nil then
      return value
    end
  end
  return nil
end

---Checks whether a path is absolute
---@param path string
---@return boolean
local function isAbsolutePath(path)
  return path:match("^/") ~= nil or path:match("^%a:[/\\]") ~= nil
end

---Checks whether a file exists
---@param path string
---@return boolean
local function fileExists(path)
  local file = io.open(path, "rb")
  if file == nil then
    return false
  end
  file:close()
  return true
end

---Resolves an icon path against the working directory and project directory
---@param path string|nil
---@return string|nil
local function resolveIconPath(path)
  local iconPath = metaValueToString(path)
  if iconPath == nil then
    return nil
  end
  if isAbsolutePath(iconPath) then
    return fileExists(iconPath) and iconPath or nil
  end
  if fileExists(iconPath) then
    return iconPath
  end
  if quarto ~= nil and quarto.project ~= nil and quarto.project.directory ~= nil then
    local projectPath = pandoc.path.join({ quarto.project.directory, iconPath })
    if fileExists(projectPath) then
      return projectPath
    end
  end
  return nil
end

---Adds explicit SVG dimensions when only a viewBox is present
---@param svg string
---@return string
local function normalizeSvgRootDimensions(svg)
  local openTag = svg:match("<svg[^>]*>")
  if openTag == nil then
    return svg
  end

  local hasWidth = openTag:match("%swidth%s*=") ~= nil
  local hasHeight = openTag:match("%sheight%s*=") ~= nil
  if hasWidth and hasHeight then
    return svg
  end

  local viewBox = openTag:match("viewBox%s*=%s*\"([^\"]+)\"") or openTag:match("viewBox%s*=%s*'([^']+)'")
  if viewBox == nil then
    return svg
  end

  local _, _, width, height = viewBox:find(
    "^%s*[%+%-]?[%d%.eE]+[%s,]+[%+%-]?[%d%.eE]+[%s,]+([%+%-]?[%d%.eE]+)[%s,]+([%+%-]?[%d%.eE]+)%s*$"
  )
  if width == nil or height == nil then
    return svg
  end

  local dimensions = ""
  if not hasWidth then
    dimensions = dimensions .. string.format(' width="%s"', width)
  end
  if not hasHeight then
    dimensions = dimensions .. string.format(' height="%s"', height)
  end
  local newOpenTag = openTag:gsub("<svg", "<svg" .. dimensions, 1)
  return svg:gsub(openTag, newOpenTag, 1)
end

---Returns a CSS url(...) value containing a base64-encoded image
---@param path string|nil
---@param mime string
---@return string|nil
local function cssDataUrlForIcon(path, mime)
  local resolvedPath = resolveIconPath(path)
  if resolvedPath == nil then
    return nil
  end

  local file = io.open(resolvedPath, "rb")
  if file == nil then
    return nil
  end
  local bytes = file:read("*all")
  file:close()
  if bytes == nil or bytes == "" or quarto == nil or quarto.base64 == nil or quarto.base64.encode == nil then
    return nil
  end
  if mime == "image/svg+xml" then
    bytes = normalizeSvgRootDimensions(bytes)
  end
  return string.format("url('data:%s;base64,%s')", mime, quarto.base64.encode(bytes))
end

---Selects the best image icon for the current output format
---@param callout CustomCalloutDefinition
---@return string|nil
local function selectImageIconCssUrl(callout)
  if isEpubOutput() then
    return cssDataUrlForIcon(callout.epub_icon_png, "image/png") or
      cssDataUrlForIcon(callout.html_icon_png, "image/png")
  end
  return cssDataUrlForIcon(callout.html_icon_svg, "image/svg+xml") or
    cssDataUrlForIcon(callout.html_icon_png, "image/png")
end

---Checks whether a callout declares an HTML image icon
---@param callout CustomCalloutDefinition
---@return boolean
local function hasHtmlImageIcon(callout)
  return metaValueToString(callout.html_icon_svg) ~= nil or
    metaValueToString(callout.html_icon_png) ~= nil
end

---Generates CSS for all defined custom callouts
---@param isRevealJS boolean Whether the output format is RevealJS
---@return string css The generated CSS rules
local function generateCustomCSS(isRevealJS)
  local css = ""
  local prefix = isRevealJS and ".reveal " or ""
  local headerClass = (isRevealJS or isEpubOutput()) and ".callout-title" or ".callout-header"

  -- Normalize icon alignment across the HTML, RevealJS, and EPUB renderers.
  css = css .. string.format("%s.callout.callout-titled > .callout-header,\n", prefix)
  css = css .. string.format("%s.callout.callout-titled .callout-title {\n", prefix)
  css = css .. "  align-items: center;\n"
  css = css .. "}\n"
  css = css .. string.format("%s.callout.callout-titled .callout-icon-container {\n", prefix)
  css = css .. "  display: flex;\n"
  css = css .. "  align-items: center;\n"
  css = css .. "  align-self: center;\n"
  css = css .. "}\n"
  css = css .. string.format("%s.callout.callout-titled .callout-icon::before {\n", prefix)
  css = css .. "  margin-top: 0 !important;\n"
  css = css .. "  line-height: 1;\n"
  css = css .. "}\n"

  -- Translate YAML callout information for custom callouts
  for type, callout in pairs(customCallouts) do
    if callout.color then
      local color = pandoc.utils.stringify(callout.color)

      -- Base color
      css = css .. string.format("%sdiv.callout-%s.callout {\n", prefix, type)
      css = css .. string.format("  border-left-color: %s;\n", color)
      css = css .. "}\n"

      -- Header background
      css = css .. string.format("%sdiv.callout-%s.callout-style-default %s {\n", prefix, type, headerClass)
      css = css .. string.format("  background-color: %s;\n", colorToRgba(color, 0.13))
      css = css .. "}\n"

      -- Collapse Icon (not supported in RevealJS)
      if not isRevealJS then
        css = css .. string.format("div.callout-%s .callout-toggle::before {", type)
        css = css .. "  background-image: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"rgb(33, 37, 41)\" class=\"bi bi-chevron-down\" viewBox=\"0 0 16 16\"><path fill-rule=\"evenodd\" d=\"M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z\"/></svg>');"
        css = css .. "}\n"
      end

      -- Icon Styling
      css = css .. string.format("%sdiv.callout-%s.callout-style-default .callout-icon::before, %sdiv.callout-%s.callout-titled .callout-icon::before {\n", prefix, type, prefix, type)

      local imageIconUrl = selectImageIconCssUrl(callout)
      if imageIconUrl ~= nil then
        css = css .. string.format("  background-image: %s;\n", imageIconUrl)
        css = css .. "  background-size: contain;\n"
        css = css .. "  background-repeat: no-repeat;\n"
        css = css .. "  background-position: center;\n"
        css = css .. "  content: '';\n"
      elseif callout.icon_symbol then
        local icon_symbol_str = pandoc.utils.stringify(callout.icon_symbol)
        local usesTextIcon = false
        if isFontAwesomeIcon(icon_symbol_str) and canUseFontAwesome() then
          -- Font Awesome icon
          css = css .. "  font-family: 'Font Awesome 7 Free';\n"
          css = css .. "  font-weight: 900;\n"
          css = css .. "  font-style: normal;\n"
          css = css .. string.format("  content: '%s' !important;\n", fa.fa_unicode(icon_symbol_str))
          usesTextIcon = true
        elseif not isFontAwesomeIcon(icon_symbol_str) then
          -- Custom icon symbol
          css = css .. string.format("  content: '%s';\n", icon_symbol_str)
          usesTextIcon = true
        else
          -- Font Awesome webfonts are not reliably supported by EPUB readers.
          local escapedColor = color:gsub("#", "%%23")
          css = css .. string.format("  background-image: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"%s\" class=\"bi bi-exclamation-triangle\" viewBox=\"0 0 16 16\"><path d=\"M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z\"/></svg>');\n", escapedColor)
        end
        if usesTextIcon then
          css = css .. "  background-image: none;\n"
        end
      else
        -- The fallback case
        local escapedColor = color:gsub("#", "%%23")  -- Escape # in hex colors
        css = css .. string.format("  background-image: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"%s\" class=\"bi bi-exclamation-triangle\" viewBox=\"0 0 16 16\"><path d=\"M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057zm1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z\"/></svg>');\n", escapedColor)
      end

      css = css .. "}\n"

    end
  end
  return css
end


---Generates LaTeX \definecolor commands for PDF output
---@return string latex The LaTeX color definitions
local function generatePdfStyles()
  local latex = ""
  for type, callout in pairs(customCallouts) do
    if callout.color then
      local hex = colorToHex(pandoc.utils.stringify(callout.color))
      if hex then
        latex = latex .. string.format(
          "\\definecolor{quarto-callout-%s-color}{HTML}{%s}\n", type, hex
        )
        latex = latex .. string.format(
          "\\definecolor{quarto-callout-%s-color-frame}{HTML}{%s}\n", type, hex
        )
      end
    end
  end
  return latex
end

---Generates Typst color definitions for Typst output
---@return string typst The Typst style definitions
local function generateTypstStyles()
  local typst = ""
  for type, callout in pairs(customCallouts) do
    if callout.color then
      local hex = colorToHex(pandoc.utils.stringify(callout.color))
      if hex then
        typst = typst .. string.format(
          '#let quarto-callout-%s-color = rgb("#%s")\n', type, hex
        )
        typst = typst .. string.format(
          '#let quarto-callout-%s-color-frame = rgb("#%s")\n', type, hex
        )
      end
    end
  end
  return typst
end

---Parses custom callout definitions from document metadata
---@param meta pandoc.Meta The document metadata
local function parseCustomCallouts(meta)
  if not meta['custom-callout'] then return meta end

  for k, v in pairs(meta['custom-callout']) do
    if type(v) == "table" then
      local htmlIcon = firstNonNil(
        metaLookupPath(v, { "html", "icon" }),
        v["html-icon"]
      )
      local htmlIconPng = firstNonNil(
        metaLookupPath(v, { "html", "icon", "png" }),
        v["html-icon-png"]
      )
      local htmlIconSvg = firstNonNil(
        metaLookupPath(v, { "html", "icon", "svg" }),
        v["html-icon-svg"]
      )
      local htmlIconPath = metaValueToString(htmlIcon)
      if htmlIconPath ~= nil then
        if htmlIconSvg == nil and htmlIconPath:lower():match("%.svg$") then
          htmlIconSvg = htmlIcon
        elseif htmlIconPng == nil then
          htmlIconPng = htmlIcon
        end
      end

      local epubIcon = firstNonNil(
        metaLookupPath(v, { "epub", "icon" }),
        v["epub-icon"]
      )
      local epubIconPng = firstNonNil(
        metaLookupPath(v, { "epub", "icon", "png" }),
        v["epub-icon-png"]
      )
      if epubIconPng == nil and type(epubIcon) ~= "table" then
        epubIconPng = epubIcon
      end

      customCallouts[k] = {
        type = tostring(k),
        title = v.title or k:gsub("^%l", string.upper),
        icon = v.icon == 'true' or nil,
        appearance = v.appearance or nil,
        collapse = v.collapse or nil,
        icon_symbol = v['icon-symbol'] or nil,
        html_icon_png = htmlIconPng,
        html_icon_svg = htmlIconSvg,
        epub_icon_png = epubIconPng,
        color = v.color or nil,
        background_color = v['background-color'] or nil
      }
    end
  end


  -- Detect format and inject appropriate styles
  local isRevealJS = quarto.doc.is_format("revealjs")
  if isEpubOutput() then
    local customCSS = generateCustomCSS(false)
    if customCSS ~= "" then
      attachEpubCss(meta, customCSS)
    end
  elseif quarto.doc.is_format("html") or isRevealJS then
    local customCSS = generateCustomCSS(isRevealJS)
    if customCSS ~= "" then
      quarto.doc.include_text('in-header', '<style>\n' .. customCSS .. '</style>')
    end
    -- Load FontAwesome font dependency (HTML only)
    for _, callout in pairs(customCallouts) do
      if not hasHtmlImageIcon(callout) and callout.icon_symbol and isFontAwesomeIcon(pandoc.utils.stringify(callout.icon_symbol)) then
        ensureFontAwesomeDeps()
        break
      end
    end
  elseif quarto.doc.is_format("pdf") then
    local pdfStyles = generatePdfStyles()
    if pdfStyles ~= "" then
      quarto.doc.include_text('in-header', pdfStyles)
    end
  elseif quarto.doc.is_format("typst") then
    local typstStyles = generateTypstStyles()
    if typstStyles ~= "" then
      quarto.doc.include_text('in-header', typstStyles)
    end
  end

  return meta
end


---Converts a div to a custom callout if it matches a defined custom callout
---@param div pandoc.Div The div to potentially convert
---@return pandoc.Div|quarto.Callout converted The converted callout or original div
local function headerToCalloutTitleInlines(header)
  local inlines = pandoc.Inlines({})
  for _, inline in ipairs(header.content) do
    if not (inline.t == "Span" and inline.classes ~= nil and inline.classes:includes("header-section-number")) then
      inlines:insert(inline)
    end
  end
  while #inlines > 0 and inlines[1].t == "Space" do
    inlines:remove(1)
  end
  return inlines
end

local function convertToCustomCallout(div)
  -- Check if the div has classes
  for _, class in ipairs(div.classes) do
    
    -- Check if the class matches a custom callout
    local callout = customCallouts[class]

    if callout then 
      -- Use the default title if not provided
      local title = callout.title

      -- Check to see if the title is specified in the div content
      if div.content[1] ~= nil and div.content[1].t == "Header" then
        title = headerToCalloutTitleInlines(div.content[1])
        div.content:remove(1)
      end

      -- Create a new Callout with the custom callout parameters
      local calloutParams = {
        type = callout.type,
        content = div.content,
        title = div.attributes.title or title,
        icon = div.attributes.icon or callout.icon,
        appearance = div.attributes.appearance or callout.appearance,
        collapse = div.attributes.collapse or callout.collapse
      }
      
      return quarto.Callout(calloutParams)
    end
  end
  

  return div
end

---Walks the Pandoc document and processes divs to
---convert to custom callouts
---@class pandoc.Doc
---@field blocks pandoc.Blocks
---@param doc pandoc.Doc The Pandoc document
---@return pandoc.Doc doc The processed document
local function customCalloutFilter(doc)

  -- Walk the AST and process divs
  doc.blocks = doc.blocks:walk({
    Div = convertToCustomCallout
  })
  
  -- Return the modified document
  return doc
end

-- Return the Pandoc filter
return {
  ---@type fun(meta: pandoc.Meta)
  Meta = parseCustomCallouts,
  ---@type fun(doc: pandoc.Doc): pandoc.Doc
  Pandoc = customCalloutFilter
}
