/* You must load the following scripts prior to calling functions in this one:
 *
 * js/jquery-3.2.1.min.js
 * js/jquery-ui.js
 * js/d3.v3.min.js
 *
 * The following css files are also recommended:
 *
 * css/jquery-ui.css
 *
 */

function init_table_data(json_file, sources) {
  sources = sources || [];

  oncolor="#11CC11";
  offcolor="#AAAAAA";
  show_credibility = [0.0, 100.0]; // min, max
  show_bias = [0.0, 100.0]; // min, max
  show_subjectivity = [0.0, 100.0, 0.0, 100.0]; // min_title_subj, max_title_subj, min_text_subj, max_text_subj
  show_community = [0.0, 100.0]; // min, max
  
  table_columns = ["Credibility", "Political Impartiality", "Title", "Source", "Title Objectivity", "Text Objectivity", "Community Rating", "URL"];
  
  sort_value = 3;
  sort_reverse = false;
  expanded_row = false;
  
  d3.json(json_file, function(error, data) {

    /* Find our data */
    if (sources.length == 0) {
      all_data = data.urls;
    }
    else {
      all_data = data.urls.filter(function (d) {
        if (sources.includes(d.source)) {
          return true;
        }
        return false;
      });
    }
  
    article_table = d3.select("#article_table")
                      .append("table")
                      .attr("width", "100%")
                      .attr("border", "0");

    article_table.append("thead")
                 .selectAll("th")
                 .data(table_columns)
                 .enter()
                 .append("th")
                 .append("td")
                 .attr("align", "left")
                 .text(function(d) { return d; })
                 .on("click", function (d, i) { sort_table_column(i) });

    setup_article_table();
  });

}

function init_sliders() {
  $( function() {
    $( "#credibility-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#credibility-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_credibility[0] = ui.values[0];
        show_credibility[1] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#credibility-slider-vals" ).val( $( "#credibility-slider" ).slider( "values", 0 ) +
      " - " + $( "#credibility-slider" ).slider( "values", 1 ) );
    show_credibility[0] = $("#credibility-slider").slider("values", 0);
    show_credibility[1] = $("#credibility-slider").slider("values", 1);
  } );

  $( function() {
    $( "#bias-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#bias-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_bias[0] = ui.values[0];
        show_bias[1] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#bias-slider-vals" ).val( $( "#bias-slider" ).slider( "values", 0 ) +
      " - " + $( "#bias-slider" ).slider( "values", 1 ) );
    show_bias[0] = $("#bias-slider").slider("values", 0);
    show_bias[1] = $("#bias-slider").slider("values", 1);
  } );

  $( function() {
    $( "#title-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#title-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_subjectivity[0] = ui.values[0];
        show_subjectivity[1] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#title-slider-vals" ).val( $( "#title-slider" ).slider( "values", 0 ) +
      " - " + $( "#title-slider" ).slider( "values", 1 ) );
    show_subjectivity[0] = $("#title-slider").slider("values", 0);
    show_subjectivity[1] = $("#title-slider").slider("values", 1);
  } );
  
  $( function() {
    $( "#text-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#text-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_subjectivity[2] = ui.values[0];
        show_subjectivity[3] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#text-slider-vals" ).val( $( "#text-slider" ).slider( "values", 0 ) +
      " - " + $( "#text-slider" ).slider( "values", 1 ) );
    show_subjectivity[2] = $("#title-slider").slider("values", 0);
    show_subjectivity[3] = $("#title-slider").slider("values", 1);
  } );

  $( function() {
    $( "#community-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#community-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_community[0] = ui.values[0];
        show_community[1] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#community-slider-vals" ).val( $( "#community-slider" ).slider( "values", 0 ) +
      " - " + $( "#community-slider" ).slider( "values", 1 ) );
    show_community[0] = $("#community-slider").slider("values", 0);
    show_community[1] = $("#community-slider").slider("values", 1);
  } );
}

function fill_in_table_data(rows) {
  var tdata = rows.selectAll("td")
      .data(function(d) {return d;})

  tdata.enter()
       .append("td")

  /* We can add images, links, or text here, so we have to do this as a
   * function
   */
  tdata.each(function(d) {
        var val = d3.select(this);
        val.selectAll("*").remove();
        if (typeof d == 'string') {
	  if (d.startsWith("http")) {
            val.append("a")
               .attr("href", d)
               .text(d);
	  }
	  else {
            val.text(d);
	  }
        }
        else {
          if (typeof d == 'number') {
	    d = color_result(d)
          }
          item = val.append(d.type);
          for (attr in d.attrs) {
            item.attr(attr, d.attrs[attr])
          }
          if ('text' in d) {
            item.text(d.text);
          }
        }
      });

  tdata.exit().remove();
}

function add_buttons(tag, values) {
  /* add grey/green buttons at the top that let the analyst turn on/off buttons
   * of interest. When these buttons are off, the matching entries will be
   * omitted from the article table.
   */

  function click_buttons() {
    var info = d3.select(this).datum()
  
    // Turn off the button
    if (info[1]) {
      info[1] = false;
    }
    else {
      d3.select(this)
        .attr("bgcolor", oncolor);
      info[1] = true;
    }
  
    d3.select(this)
      .attr("bgcolor", function(d) { return d[1] ? oncolor : offcolor; });
  
    var ret = []
    values.forEach(function(d) {
      if (d[1]) {
        ret.push(d[0]);
      }
    });
  
    setup_article_table();
  }

  buttons = d3.select(tag)
              .append("table")
              .attr("width", "100%")
              .append("tbody")
              .append("tr");

  buttons.selectAll("td")
         .data(values)
         .enter()
           .append("td")
           .attr("id", function(d) { return "button-" + d[0]; })
           .attr("bgcolor", function(d) { return d[1] ? oncolor : offcolor; })
           .on("click", click_buttons)
           .append("center")
           .append("b")
           .text(function(d) { return d[0]; });

  return buttons;
}

function sort_table_column(sort_index) {
  if (sort_index != sort_value || sort_reverse) {
    sort_value = sort_index;
    sort_reverse = false;
  }
  else {
    sort_reverse = true;
  }

  setup_article_table();
}

function get_credibility_filter_result(d) {
  return d.classifiers[0].result;
}

function get_bias_filter_result(d) {
  return d.classifiers[1].result;
}

function get_community_filter_result(d) {
  return d.classifiers[2].result;
}

function get_subjectivity_result(d) {
  return d.classifiers[3].result;
}

function clear_expanded_row() {
  article_table.selectAll("#details-row").remove();
  expanded_row = false;
}

function expand_row(d, i) {
  parent = d3.select(this.parentNode);
  parent.selectAll("#details-row").remove();

  url = d[d.length-1].attrs.href;
  if (expanded_row == url) {
    expanded_row = false;
    return;
  }

  expanded_row = url;

  /* Find our data */
  info = false
  all_data.some(function (d) {
    if (d.url == url) {
      info = d;
      return true;
    }
    return false;
  })

  div = parent.insert("tr", "#info-row-" + i + "+*")
              .attr("id", "details-row")
              .append("td")
              .attr("colspan", d.length)
              .append("p")
              .append("div")
              .style("border-style", "outset")
              .style("border-width", 1)

  div.append("font")
     .text(url)
  div.append("p")

  /* Fake Filter Results */
  div.append("h3")
     .text("Credibility Filter:")
  get_credibility_filter_result(info).forEach(function (a) {
    div.append("font")
       .text(a[0] + ": " + a[1])
    div.append("br")
  });
  div.append("p")

  /* Impartiality Filter Results */
  div.append("h3")
     .text("Political Impartiality Filter:")
  get_bias_filter_result(info).forEach(function (a) {
    div.append("font")
       .text(a[0] + ": " + a[1])
    div.append("br")
  });
  div.append("p")

  /* Community Filter Results */
  div.append("h3")
     .text("Community Rating Filter:")
  get_community_filter_result(info).forEach(function (a) {
    div.append("font")
       .text(a[0] + ": " + a[1])
    div.append("br")
  });
  div.append("p")

  /* Article Text */
  div.append("h3")
     .text("Article Text:")
  div.append("font")
     .text(info.text)
  div.append("p")

  /* Remove Entry Button */
  div.append("form")
     .attr("action", "/remove")
     .attr("method", "POST")
     .append("button")
       .attr("type", "submit")
       .attr("name", "url")
       .attr("value", url)
       .text("Remove Entry")
  div.append("p")
}
  
function get_perc_str(value) {
  return Math.round(value * 100).toString() + "%";
}

function color_result(value) {
  if (value < .4) {
    color = 'red';
  }
  else if (value < .6) {
    color = 'orange';
  }
  else {
    color = 'green';
  }
  return {type:"font", attrs:{color:color}, text:get_perc_str(value)}
}

function setup_article_table() {
  clear_expanded_row();

  table_values = []

  /* Apply filters to the data:
   * (1) Remove real/fake/satire data as requested
   * (2) Only use data with popularity/engagement values above 0 for
   *     communities the analyst is interested in.
   * (3) Remove data that does not fit within the double slider values of
   *     subjectivity.
   */
  var filtered_data = all_data.filter(function(d) {
    /* Credibility filters */
    credibility = get_credibility_filter_result(d)[1][1];
    if (credibility * 100 < show_credibility[0] || credibility * 100 > show_credibility[1]) {
      return false;
    }

    /* Impartiality filters */
    bias = get_bias_filter_result(d)[1][1];
    if (bias * 100 < show_bias[0] || bias * 100 > show_bias[1]) {
      return false;
    }

    subj = get_subjectivity_result(d);
    if (subj[0] * 100 < show_subjectivity[0] || subj[0] * 100 > show_subjectivity[1]) {
      return false;
    }
    else if (subj[1] * 100 < show_subjectivity[2] || subj[1] * 100 > show_subjectivity[3]) {
      return false;
    }

    /* Community filters */
    community = get_community_filter_result(d)[0][1];
    if (community * 100 < show_community[0] || community * 100 > show_community[1]) {
      return false;
    }

    return true;
  });

  filtered_data.forEach(function (d, i) {
    // first check if we are filtering out this data
    
    entry = []

    /* Screen Shot Thumbnail
    if ("screenshot" in d) {
      entry.push({type:"img", attrs:{src:d.screenshot}})
    }
    */

    /* Credibility Filter */
    credibility = parseFloat(get_credibility_filter_result(d)[1][1])
    entry.push(color_result(credibility));

    /* Impartiality Filter */
    bias = parseFloat(get_bias_filter_result(d)[1][1])
    entry.push(color_result(bias));

    /* Title */
    entry.push(d.title);

    /* Source */
    entry.push(d.source);

    /* Objectivity Measure */
    subj = get_subjectivity_result(d);
    entry.push(color_result(subj[0]));
    entry.push(color_result(subj[1]));

    /* Community Filter */
    community = parseFloat(get_community_filter_result(d)[0][1])
    entry.push(color_result(community));

    /* Link to article */
    entry.push({type:"a", attrs:{href:d.url, target:"_blank"}, text:'Link'});

    table_values.push(entry);
  });

  table_values.sort(function(a, b) {
    a_val = parseInt(a[sort_value]);
    b_val = parseInt(b[sort_value]);

    if (isNaN(a_val) || isNaN(b_val)) {
      a_val = a[sort_value];
      b_val = b[sort_value];
    }

    if (typeof a_val === 'object') {
      a_val = a_val.text;
    }

    if (typeof b_val === 'object') {
      b_val = b_val.text;
    }

    ret = 0;
    if (a_val < b_val) {
      ret = -1;
    }
    else if (a_val > b_val) {
      ret = 1;
    }

    if (sort_reverse) {
      ret = ret * -1;
    }

    return ret;
  });

  var rows = article_table.selectAll("tr")
                          .data(table_values)

  rows.enter()
      .append("tr")
      .attr("id", function(d, i) { return "info-row-" + i} )
      .attr("bgColor", "#FFFFFF")
      .on("click", expand_row)
      .on("mouseover", function() { d3.select(this).attr("bgColor","#CCCCCC"); })
      .on("mouseout", function() { d3.select(this).attr("bgColor","#FFFFFF"); })

  fill_in_table_data(rows);

  rows.exit().remove();

  //create_graph(table_values);
}

function create_graph(table_values) {
  create_pie(table_values, "Credibility", ["Reliable", "Unreliable"], 0);
}

function create_pie(table_values, name, labels, index) {
  charts = d3.select("#charts");
  charts.selectAll("#" + name).remove();
  charts.append("div")
        .attr("id", name)
        .style("width", "30%");

  values = []
  for (j in labels) {
    values.push(0);
  }

  pie = [{values:values, labels:labels, type:'pie'}];
  layout = {title:name, height:300, width:300};

  table_values.forEach(function(a, i) {
    for (j in pie[0].labels) {
      if (a[index].text == pie[0].labels[j]) {
        pie[0].values[j]++;
      }
    }
  });

  Plotly.newPlot(name, pie, layout);
}


