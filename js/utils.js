/*
 * The MIT License (MIT)
 * 
 * Copyright (c) 2015 Juan Cruz-Benito. http://juancb.es
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

function add_y_axis(canvas, y, range, domain, ticks = 8) {
  var yAxis = d3.svg.axis()
      .scale(y)
      .ticks(ticks)
      .orient("left")

  canvas.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .selectAll("text")
        .style("font-size", ".6em")

  return y
}

function add_x_axis(canvas, x, height, ticks = 8) {
  var xAxis = d3.svg.axis()
      .scale(x)
      .ticks(ticks)
      .orient("bottom")

  canvas.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")
        .style("font-size", ".6em")

  return x
}

function add_legend(canvas, data, xoffset, yoffset) {
    var legend = canvas.selectAll(".legend")
        .data(data)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(" + xoffset + "," + (yoffset + i * 20) + ")"; });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function(d) {
          if ("color" in d) {
              return d.color;
          }
          return "steelblue";
        });

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d.xval; });
}

/* Expected data passed into this function is a list of dictionaries containing
 * {xval, yval, key}. The key value is used to determine where the values are
 * places on the x axis.
 */
function line_chart(canvas, data, xaxis = true, yaxis = true) {
  var xdomain = [0, d3.max(data, function(d) { return d.key})]
  var ydomain = d3.extent(data, function(d) {return d.yval})
  ydomain[0] = 0

  var x = d3.scale.linear()
      .range([0, graph_width])
      .domain(xdomain)

  var y = d3.scale.linear()
      .range([0, graph_height])
      .domain(ydomain.reverse())

  if (xaxis) {
    add_x_axis(canvas, x, graph_height);
  }

  if (yaxis) {
    add_y_axis(canvas, y);
  }

  // used to generate a line from a path
  var line = d3.svg.line()
      .x(function (d) { return x(d.key) })
      .y(function (d) { return y(d.yval) })

  var path = canvas.append("g").append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1.5)
      .attr("d", line);
}

/* Expected data passed into this function is a list of dictionaries containing
 * {xval, yval, key}. The key value is used to determine where the values are
 * places on the x axis.
 */
function bar_chart(canvas, title, data, bar_width = 20, xaxis_ticks = 8, yaxis_ticks = 8) {
  var svg = canvas.append("svg")
      .attr("width", "99%")
      .attr("height", "99%");

  var width = parseInt(svg.style("width")) * 0.6;
  var height = parseInt(svg.style("height")) * 0.6;

  var g = svg.append("g")
      .attr("transform", "translate(" + width / 4 + "," + height / 4 + ")")

  var xdomain = [-0.5, d3.max(data, function(d) { return d.key + 0.5 })]
  var ydomain = d3.extent(data, function(d) {return d.yval + 0.5 })
  ydomain[0] = 0

  var x = d3.scale.linear()
      .range([0, width])
      .domain(xdomain)

  var y = d3.scale.linear()
      .range([0, height])
      .domain(ydomain.reverse())

  add_x_axis(g, x, height, xaxis_ticks);
  add_y_axis(g, y, yaxis_ticks);
  add_legend(g, data, width * 1.2, height / 2);

  // Title
  g.append("text")
      .attr("x", width / 2)
      .attr("y", height + 30)
      // the dx/dy attribute moves the text
      .attr("fill", "#000")
      .attr("text-anchor", "middle")
      .text(title)

  var bars = g.selectAll(".bar")
      .data(data)
      .enter()
        .append("g")
        .attr("class", "bar")

  bars.append("rect")
      .attr("x", function(d) { return x(d.key) })
      .attr("y", function(d) { return height })
      .attr("width", bar_width)
      .attr("height", 0)
      //.attr("height", function(d) { return height - y(d.yval) })
      .attr("fill", function(d) {
          if ("color" in d) {
              return d.color;
          }
          return "steelblue";
      })
      .transition()
        // remove the transition for now
        .duration(0)
        .attr("y", function(d) { return y(d.yval) })
        .attr("height", function(d) { return height - y(d.yval) })

  bars.append("text")
      .attr("x", function (d) { return x(d.key) })
      .attr("y", function (d) { return y(d.yval) })
      // the dx/dy attribute moves the text
      .attr("dx", function(d) { return bar_width/2 })
      .attr("dy", "10px")
      .attr("fill", "#FFF")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.yval })
}

class DonutChart {
  constructor(canvas, title, radius = 150) {
    this.width = parseInt(canvas.style("width")) * 0.5;
    this.height = parseInt(canvas.style("height")) * 0.4;
    this.radius = radius;

    this.svg = canvas.append("svg")
        .attr("width", "99%")
        .attr("height", "99%")
        .append("g")
        .attr("transform", "translate(" + this.width + "," + this.height + ")");

    // Title
    this.svg.append("text")
        .attr("x", 0)
        .attr("y", 0)
        // the dx/dy attribute moves the text
        .attr("fill", "#000")
        .attr("text-anchor", "middle")
        .text(title)

    this.svg.append("g")
    	.attr("class", "slices");
    this.svg.append("g")
    	.attr("class", "labelName");
    this.svg.append("g")
    	.attr("class", "labelValue");
    this.svg.append("g")
    	.attr("class", "lines");

    this.pie = d3.layout.pie()
    	.sort(null)
    	.value(function(d) {
    		return d.yval;
    	});
    
    this.arc = d3.svg.arc()
    	.outerRadius(this.radius * 0.8)
    	.innerRadius(this.radius * 0.4);
    
    this.outerArc = d3.svg.arc()
    	.innerRadius(this.radius * 0.9)
    	.outerRadius(this.radius * 0.9);
    
    this.legendRectSize = (this.radius * 0.05);
    this.legendSpacing = this.radius * 0.02;
    
    this.div = this.svg.append("div")
        .attr("class", "tooltip")
        .style("display", "none");
    
    var colorRange = d3.scale.category20();
    this.color = d3.scale.ordinal()
    	.range(colorRange.range());

  }
    
  /* Expected data passed into this function is a list of dictionaries containing
   * {xval, yval, color}. Matching x values will be grouped together.
   */
  change(data) {
      var chart = this;
      var div = this.div;

      //add_legend(this.svg, data, 0, 0);

      /*
      var total = 0;

      data.forEach(function(d, i) {
          total += d.yval;
      });
      */
 
      /* ------- PIE SLICES -------*/
      var slice = chart.svg.select(".slices").selectAll("path.slice")
          .data(chart.pie(data), function(d){ return d.data.xval });
  
      slice.enter()
          .insert("path")
          .style("fill", function(d) { 
              if ("color" in d.data) {
                  return d.data.color;
              }
              return chart.color(d.data.xval); 
          })
          .attr("class", "slice");
  
      slice
          .transition().duration(1000)
          .attrTween("d", function(d) {
              this._current = this._current || d;
              var interpolate = d3.interpolate(this._current, d);
              this._current = interpolate(0);
              return function(t) {
                  return chart.arc(interpolate(t));
              };
          })

      /* Not working, probably unnecessary too
      slice
          .on("mousemove", function(d){
              div
                  .style("left", (d3.event.pageX - 34) + "px")
                  .style("top", (d3.event.pageY - 12) + "px")
                  .style("display", "inline-block")
                  .html((d.data.xval)+"<br>"+(d.data.yval)+"%");
          });
      slice
          .on("mouseout", function(d){
              div.style("display", "none");
          });
      */
  
      slice.exit()
          .remove();
  
      /*
      var legend = chart.svg.selectAll('.legend')
          .data(chart.color.domain())
          .enter()
          .append('g')
          .attr('class', 'legend')
          .attr('transform', function(d, i) {
              var height = chart.legendRectSize + chart.legendSpacing;
              var offset =  height * chart.color.domain().length / 2;
              var horz = -3 * chart.legendRectSize;
              var vert = i * height - offset;
              return 'translate(' + horz + ',' + vert + ')';
          });
  
      legend.append('rect')
          .attr('width', chart.legendRectSize)
          .attr('height', chart.legendRectSize)
          .style('fill', chart.color)
          .style('stroke', chart.color);
  
      legend.append('text')
          .attr('x', chart.legendRectSize + chart.legendSpacing)
          .attr('y', chart.legendRectSize - chart.legendSpacing)
          .text(function(d) { return d; });
      */
  
      /* ------- TEXT LABELS -------*/
  
      var text = chart.svg.select(".labelName").selectAll("text")
          .data(chart.pie(data), function(d){ return d.data.xval });
  
      text.enter()
          .append("text")
          .attr("dy", ".35em")
          .text(function(d) {
              return (d.data.xval+": "+d.data.yval);
          });
  
      function midAngle(d){
          return d.startAngle + (d.endAngle - d.startAngle)/2;
      }
  
      text
          .transition().duration(1000)
          .attrTween("transform", function(d) {
              this._current = this._current || d;
              var interpolate = d3.interpolate(this._current, d);
              this._current = interpolate(0);
              return function(t) {
                  var d2 = interpolate(t);
                  var pos = chart.outerArc.centroid(d2);
                  pos[0] = chart.radius * (midAngle(d2) < Math.PI ? 1 : -1);
                  return "translate("+ pos +")";
              };
          })
          .styleTween("text-anchor", function(d){
              this._current = this._current || d;
              var interpolate = d3.interpolate(this._current, d);
              this._current = interpolate(0);
              return function(t) {
                  var d2 = interpolate(t);
                  return midAngle(d2) < Math.PI ? "start":"end";
              };
          })
          .text(function(d) {
              return (d.data.xval+": "+d.data.yval);
          });
  
  
      text.exit()
          .remove();
  
      /* ------- SLICE TO TEXT POLYLINES -------*/
/*  
      var polyline = chart.svg.select(".lines").selectAll("polyline")
          .data(chart.pie(data), function(d){ return d.data.xval });
  
      polyline.enter()
          .append("polyline");
  
      polyline.transition().duration(1000)
          .attrTween("points", function(d){
              this._current = this._current || d;
              var interpolate = d3.interpolate(this._current, d);
              this._current = interpolate(0);
              return function(t) {
                  var d2 = interpolate(t);
                  var pos = chart.outerArc.centroid(d2);
                  pos[0] = chart.radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
                  return [chart.arc.centroid(d2), chart.outerArc.centroid(d2), pos];
              };
          });
  
      polyline.exit()
          .remove();
*/
  }
}

function add_table(canvas, data, headers = null) {

  var table = canvas.append("table")

  if (headers) {
    var thead = table.append('thead')
    thead.append("tr").selectAll("th")
        .data(headers)
      .enter().append("th")
        .text(function(d) { return d; });
  }

  var tbody = table.append('tbody');

  tr = tbody.selectAll("tr")
       .data(data)
    .enter().append("tr")

  tr.selectAll("td")
       .data(function(d) { return d; })
    .enter().append("td")
       .text(function(d) { return d; });

  return table;
}

function split_canvas_horizontal(canvas, num_splits) {
    ret = [];
    width = 100 / num_splits;
    for (i = 0; i < num_splits; i++) {
        var div = canvas.append("div")
            .attr("style", "float: left; display: inline-block; width: " + width + "%; height: 100%");
        ret.push(div);
    }

    return ret;
}
