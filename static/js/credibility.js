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

function init_table_data(json_file, filters, sources) {
  sources = sources || [];

  oncolor="#11CC11";
  offcolor="#AAAAAA";
  show_reliability = [0.0, 100.0]; // min, max
  show_bias = [0.0, 100.0]; // min, max
  show_subjectivity = [0.0, 100.0, 0.0, 100.0]; // min_title_subj, max_title_subj, min_text_subj, max_text_subj
  show_community = [0.0, 100.0]; // min, max
  
  table_columns = ["Reliability", "Political Impartiality", "Title", "Source", "Title Objectivity", "Text Objectivity", "Most Interested Community", "URL"];
  
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

    if (filters) {
      init_filters(all_data);
    }

    setup_article_table();

  });
}

function init_filters(data) {
  $( function() {
    $( "#reliability-slider" ).slider({
      range: true,
      min: 0,
      max: 100,
      values: [ 0, 100 ],
      slide: function( event, ui ) {
        $( "#reliability-slider-vals" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        show_reliability[0] = ui.values[0];
        show_reliability[1] = ui.values[1];
        setup_article_table();
      }
    });
    $( "#reliability-slider-vals" ).val( $( "#reliability-slider" ).slider( "values", 0 ) +
      " - " + $( "#reliability-slider" ).slider( "values", 1 ) );
    show_reliability[0] = $("#reliability-slider").slider("values", 0);
    show_reliability[1] = $("#reliability-slider").slider("values", 1);
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

  /*
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
  */

  /* Grab the various community names, adding 'r/news' */
  communities = [['r/news', true]]; /* globally declared */
  get_community_filter_result(data[0]).forEach(function(d) {
    communities.push([d[0].split(" ")[1], true]);
  });

  add_buttons('Community Filters', '#filters_div', communities);
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

function add_buttons(title, tag, values) {
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

  d3.select(tag).append("br");

  d3.select(tag)
    .append("label")
    .text(title);

  buttons = d3.select(tag)
              .append("table")
              .style("width", "100%")
              .style("padding", "20px")
              .append("tbody")
              .append("tr")

  buttons.selectAll("td")
         .data(values)
         .enter()
           .append("td")
           .style("border", "3px solid #FFFFFF")
           .style("border-radius", "50px")
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

function get_filter_result(d, name) {
  return d.classifiers[d.cindex[name]].result;
}

function get_reliability_filter_result(d) {
  return get_filter_result(d, "fake_filter");
}

function get_bias_filter_result(d) {
  return get_filter_result(d, "bias_filter");
}

function get_community_filter_result(d) {
  return get_filter_result(d, "community_filter");
}

function get_highest_community_rating(d) {
  var test = 0.5;
  var ret = 'r/news';

  var result = get_community_filter_result(d);
  for (i in result) {
    var value = parseFloat(result[i][1]);
    if (value > test) {
      ret = result[i][0].split(" ")[1];
      test = value;
    }
  }

  return ret;
}

function get_subjectivity_result(d) {
  return get_filter_result(d, "subjectivity_classifier");
}

function clear_expanded_row() {
  article_table.selectAll("#details-row").remove();
  expanded_row = false;
}

function clear_row() {
  d3.selectAll("#details-row").remove();
  expanded_row = false;
}

function chartAnalysis(div, id, title, data) {
  div.append("div")
     .attr("height", "100")
     .attr("id", id)

  /* Data Example:
   * [
   * ['Task', 'Hours per Day'],
   * ['Work',     11],
   * ['Eat',      2],
   * ['Commute',  2],
   * ['Watch TV', 2],
   * ['Sleep',    7]
   * ]
   */

  var dataPoints = [['Type', 'Probability', {role:'annotation'}]];
  data.forEach(function (a) {
    dataPoints.push([a[0], parseFloat(a[1]), a[1]]);
  });

  var type = "Bar";
  var options = {hAxis: {minValue:0, maxValue:1}};

  drawChart(type, id, title, dataPoints, options);
}

function expand_row(d, i) {
  parent = d3.select(this.parentNode);
  parent.selectAll("#details-row").remove();

  var url = d[d.length-1].attrs.href;
  if (expanded_row == url) {
    expanded_row = false;
    return;
  }

  expanded_row = url;

  /* Find our data */
  var info = false
  all_data.some(function (d) {
    if (d.url == url) {
      info = d;
      return true;
    }
    return false;
  })

  var div = parent.insert("tr", "#info-row-" + i + "+*")
              .attr("id", "details-row")
              .append("td")
              .attr("colspan", d.length)
              .append("p")
              .append("div")
              .style("border-style", "outset")
              .style("border-width", 1)

  /* Reliability and Impartiality Results */
  var results = [];
  results.push(["Title Objectivity", get_subjectivity_result(info)[0]]);
  results.push(["Text Objectivity", get_subjectivity_result(info)[1]]);
  results.push(get_reliability_filter_result(info)[1]);
  results.push(get_bias_filter_result(info)[1]);
  chartAnalysis(div, "writing_style_div", "Writing Style Analysis", results);

  /* Community Filter Results */
  chartAnalysis(div, "comm_div", "Community Ratings", get_community_filter_result(info));

  /* Article Text */
  div.append("h3")
     .text("Article Text:")
  div.append("font")
     .text(info.text)
  div.append("p")

  /* Article URL */
  div.append("h3")
     .text("Article URL:")
  div.append("a")
     .attr("href", url)
     .text(url)
  div.append("p")

  /* Remove Entry Button */
  var tr = div.append("table")
              .append("tbody").append("tr");

  tr.append("td").append("form")
     .attr("action", "/remove")
     .attr("method", "POST")
     .append("button")
       .attr("type", "submit")
       .attr("name", "url")
       .attr("value", url)
       .text("Remove Entry");

  /* Remove Entry Button */
  tr.append("td").append("input")
     .attr("type", "button")
     .attr("onclick", "clear_row()")
     .attr("value", "Hide");

  div.append("p");
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
    /* Reliability filters */
    reliability = get_reliability_filter_result(d)[1][1];
    if (reliability * 100 < show_reliability[0] || reliability * 100 > show_reliability[1]) {
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
    //community = 1 - parseFloat(get_community_filter_result(d)[0][1])
    //if (community * 100 < show_community[0] || community * 100 > show_community[1]) {
    //  return false;
    //}
    var community = get_highest_community_rating(d);
    var test = true;

    /* look at the communities buttons and see if this one is on/off */
    communities.some(function(d) {
      if (d[0] == community) {
        test = d[1];
        return true;
      }
      return false;
    });

    if (!test) {
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

    /* Reliability Filter */
    reliability = parseFloat(get_reliability_filter_result(d)[1][1])
    entry.push(color_result(reliability));

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
    //community = 1 - parseFloat(get_community_filter_result(d)[0][1])
    //entry.push(color_result(community));
    community = get_highest_community_rating(d);
    entry.push(community);

    /* Link to article */
    entry.push({type:"a", attrs:{href:d.url, target:"_blank"}, text:'Link'});

    table_values.push(entry);
  });

  table_values.sort(function(a, b) {
    var a_val = a[sort_value];
    var b_val = b[sort_value];
    if (typeof(a_val) === 'object') {
      a_val = a_val.text;
    }
    if (typeof(b_val) === 'object') {
      b_val = b_val.text;
    }

    var a_num = parseFloat(a_val);
    var b_num = parseFloat(b_val);

    if (!isNaN(a_num) && !isNaN(b_num)) {
      a_val = a_num;
      b_val = b_num;
    }

    var ret = 0;
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
}
