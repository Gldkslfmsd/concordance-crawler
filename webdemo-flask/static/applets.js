/**
 * (c) 2014, Vincent Kriz, kriz@ufal.mff.cuni.cz
 * This script implements RExtractor web interface
 */

// Global variabiles
var id = "";
var content = "";
var strategy = "";

var message = "";
var highlight = "";
var box = undefined;
var timeout = undefined;

var list_start = 0;
var list_limit = 10;
var list_order_by = "ctime";
var list_order_dir = "DESC";

// Start with welcome screen
jQuery('body').ready(function() {
    applet_server_status();
    applet_text_box('home');
});

var page = "document";

// Functions in menu
function run_text(text_id) {
		page = "text";
    clear_main_column();
    applet_text_box(text_id);
}

function run_list(id_to_highlight, refresh) {
		page = "list";
    clear_main_column();
    applet_list(id_to_highlight, refresh);
}

function run_submit() {
		page = "submit";
    clear_main_column();
    applet_submit();
}

function run_document(id) {
		page = "document";
    clear_main_column();
    applet_document(id);
}

/**
 * APPLETS
 */
function applet_server_status() {
    jQuery.ajax({
        url: "/serverstatus",
        success: function(data) {
            var servers = data.split('\n');

            // Format HTML output
            var output = "";
            output += "<table>";
            for (var i = 0; i < servers.length; i++) {
                if (!servers[i].match(/(ON|OFF)/)) {
                    continue;
                }

                if (servers[i].match(/ON/)) {
                    output += "<tr><td><img src='static/green.png'></td><td>" + servers[i] + "</td></tr>";
                }
                else {
                    output += "<tr><td><img src='static/red.png'></td><td>" + servers[i] + "</td></tr>";
                }
            }
            output += "</table>";

            // Hide loading and show table
            jQuery('#applet_server_status .loading').slideUp();
            jQuery('#applet_server_status .data').html(output);
            jQuery('#applet_server_status .data').slideDown();
        },
        error: function() {
            jQuery('#applet_server_status').html("<p>Couldn't retrieve server status</p>");
        }
    });
    setTimeout('applet_server_status()', 10000);
}

function applet_text_box(text_id) {
    // Clear timeout
    clearTimeout(timeout);

    jQuery.ajax({
        url: "./static/" + text_id + ".html",
        success: function(data) {
            // Format HTML output
            var output = "";
            output += "<div class='box'>";
            output += data;
            output += "</div>";

            // Show data
            jQuery('#main-column').append(output);
            jQuery('#main-column').find('.box').each(function() {
                jQuery(this).slideDown();
            });
        },
        error: function() {
            jQuery('#applet_server_status').html("<p>Couldn't retrieve text.</p>");
        }
    });
}

function applet_list(id_to_highlight, refresh) {
    // Clear timeout
    clearTimeout(timeout);

    // Clear message
    message = "";

    var output = "";

    if (!refresh) {
        output += "<div class='box'>";
        output += "<h2>List of crawling jobs <div class='short-loading'>Loading ...</div></h2>"
        output += "<div class='loading'></div>";
        output += "<div class='message'>" + message + "</div>";
        output += "<div class='data'></div>";
        output += "</div>";

        // Hide loading and show table
        box = jQuery('#main-column').append(output);
        jQuery('#main-column').find('.box').each(function() {
            jQuery(this).slideDown();
        });
    }

    jQuery.ajax({
        url: "/listjobs/start=" + list_start + "/limit=" + list_limit + "/order_by=" + list_order_by + "/order_dir=" + list_order_dir,
        success: function(data) {
						if (page!="list") {
							return;
						}
            var jobs = data.split('\n');

            // Sorting icon
            var sorting = ["", "", ""];

            var sorting_data = jobs[1].split(",");
            if (sorting_data[3] == "id") {
                if (sorting_data[4] == "DESC") {
                    sorting[0] = "<img src='static/sort-desc.png'>";
                }
                else {
                    sorting[0] = "<img src='static/sort-asc.png'>";
                }
            }
            if (sorting_data[3] == "ctime") {
                if (sorting_data[4] == "DESC") {
                    sorting[1] = "<img src='static/sort-desc.png'>";
                }
                else {
                    sorting[1] = "<img src='static/sort-asc.png'>";
                }
            }
            if (sorting_data[3] == "status") {
                if (sorting_data[4] == "DESC") {
                    sorting[2] = "<img src='static/sort-desc.png'>";
                }
                else {
                    sorting[2] = "<img src='static/sort-asc.png'>";
                }
            }

            // Format HTML output
            var output = "";
            output += "<table class='list'>";
            output += "<tr>";
            output += "<th colspan=1><a href='javascript:list_sort(\"id\")'    > Target word</a>       " + sorting[0] + "</th>";
            output += "<th colspan=1><a href='javascript:list_sort(\"ctime\")' > Submition time</a> " + sorting[1] + "</th>";
            output += "<th colspan=3><a href='javascript:list_sort(\"status\")'> State</a>          " + sorting[2] + "</th>";
            output += "</tr>";
            for (var i = 2; i < jobs.length; i++) {
                if (!jobs[i].match(/./)) {
                    continue;
                }

                var fields = jobs[i].split(/,/);

                // Highlight selected document
                if (id_to_highlight && jobs[i].match(new RegExp("^" + id_to_highlight + "\t"))) {
                    output += "<tr class='highlight' id='document_" + fields[0] + "'>";
                }
                else {
                    output += "<tr id='" + fields[3] + "'>";
                }

                // Process icon
                var icon = "";
                if (fields[2].match(/STARTED|CREATED/)) {
                    icon = "static/greening.gif";
                }
                if (fields[2].match(/ERROR|ABORTED/)) {
                    icon = "static/red.png";
                }
                if (fields[2].match(/FINISHED/)) {
                    icon = "static/green.png";
                }

                // Progress bar
//                var state = fields[2];
                var percent = fields[4];
                //percent -= 1;
               // percent = (100 / 6) * percent;
                var color = "green"; // state.match(/FI/) ? "red" : "green"; // TODO
                var progress_bar = "<div class='state-bar-mini'><div class='state-bar-content-mini' style='width: " + percent + "%; background: " + color + "'></div></div>";

                // Fill table
                output += "<td>" + fields[0] + "</td>";
                output += "<td>" + fields[1] + "</td>";
                output += "<td><img src='" + icon + "' + alt='" + icon + "'></td>";
                output += "<td>" + progress_bar + "</td>";
                output += "<td>" + fields[2] + "</td>";
            }
            output += "</table>";

            // First line contains data for paging...
            var pagging = jobs[1].split(",");
						var min = function(a,b) {
							return a<b?a:b;
						}
            output += "<p>Presenting <b>" + (list_start + 1) + "</b> - <b>" + (min(list_start + list_limit,pagging[0])) + "</b> jobs from <b>" + pagging[0] + "</b> jobs in total. Click to row to detail.";
            if (list_start > 0) {
                output += "<a href='javascript:list_previous()'>Show previous jobs</a>";
            }
            if (list_start + list_limit < pagging[0]) {
                if (output.match(/Show previous jobs/)) {
                    output += " | ";
                }
                output += "<a href='javascript:list_next()'>Show next jobs</a>";
            }

            if (!refresh) {
                box.find('.loading').slideUp();
                box.find('.data').html(output);
                box.find('.data').slideDown();
            }
            else {
                box.find('.data').html(output);
            }

            box.find('.data').find('tr:not(:first)').each(function() {
                jQuery(this).click(function() {
                    var id = jQuery(this).attr('id');//.replace(/(.)/, ""); //TODO
                    run_document(id);
                })
            })

            jQuery('.short-loading').hide();
        },
        error: function() {
            jQuery('#applet_server_status').html("<p>Couldn't retrieve server status</p>");
        }
    });

    timeout = setTimeout("applet_list('" + id_to_highlight + "', 1)", 10000);
}

function list_previous() {
    jQuery('.short-loading').show();
    list_start -= 10;
    list_start = list_start < 0 ? 0 : list_start;
    applet_list("", 1);
}

function list_next() {
    jQuery('.short-loading').show();
    list_start += 10;
    applet_list("", 1);
}

function list_sort(order_by, order_dir) {
    jQuery('.short-loading').show();
    list_start = 0;
    if (order_by == list_order_by) {
        if (list_order_dir == "DESC") {
            list_order_dir = "ASC";
        }
        else {
            list_order_dir = "DESC";
        }
    }
    else {
        list_order_by = order_by;
        list_order_dir = "ASC";
    }

    applet_list("", 1);
}

function applet_submit() {
    // Clear timeout
    clearTimeout(timeout);

    // Form
    var form = "";

		form += "<p>Target word(s)</p>";
		form += "<input type='text' id='target' value=''>";
		form += "<p>Target word part of speech tag regex ";
		form += "<small><br><br>Fill for example \".*\" for any part of speech, \"V.*\" for verbs, \"N.*\" for nouns etc. See <a href='https://pypi.python.org/pypi/ConcordanceCrawler/'>this link</a> for more info.";
		form += "</small></p>";
		form += "<input type='text' id='pos' value='.*'>";

    form += "<p>Number of concordances:</p>";
		form += "<input type='number' id='number' min='1' max='10000' value='10'>";

		form += "<p>Maximum number of concordances per page:</p>";
		form += "<input type='number' id='max_per_page' min='1' max='10000' value='10000'>";

		form += "<p><input type='checkbox' id='disable' name='disable'>Disable English filter</p>";

		form += "<p>Bazword generator";
		form += "<small><br><br>A nonsense bazword will be added to every search engine query to increase possible number of links ";
		form += "<br>returned by search engine. Select a strategy for bazword generating.";
		form += "</small>";
		form += "</p><select id='bazgen' size='1'>";
		var bazgens = {
			'RANDOM':'random 4-letter words',
			'WIKI_ARTICLES': 'words from random Wikipedia articles',
			'WIKI_TITLES': 'words from titles of random Wikipedia articles',
			'NUMBERS': 'increasing numbers from 1'
		};
		for (baz in bazgens) {
			form += "<option value='" + baz + "'>" + bazgens[baz] + "</option>";
		}
		form += "</select>";
		form += '<p>Encoding</p>';
		var encs = {
			'ascii': 'ascii',
			'utf-8': 'utf-8',
			'any': 'any' 
		};
		form += "<select id='enc' size='1'>";
		for (enc in encs) {
			form += "<option value='" + enc + "'>" + encs[enc] + "</option>";
		}
		form += "</select><br><br>";
		
    form += "<input id='new_submit_submit' type='button' value='Submit new job' onClick='applet_submit_click()'>";

    var output = "";
    output += "<div class='box'>";
    output += "<h2>Submit new crawling job</h2>"
    output += "<div class='loading'></div>";
    output += "<div class='message'>" + message + "</div>";
    output += "<div class='form'>";
    output += form;
    output += "</div>";
    output += "<div class='data'></div>";
    output += "</div>";

    // Hide loading and show table
    box = jQuery('#main-column').append(output);
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).slideDown();
    });
    box.find('.loading').slideUp();
}

function applet_submit_click() {
    // Hide form, show loading
    jQuery('.form').slideUp();
    box.find('.loading').slideDown();

    // Read data
    number = jQuery('#number').val();
    max_per_page = jQuery('#max_per_page').val();
    disable = jQuery('#disable').is(':checked');
		post_data = "number_of_concordances="+number+"&max_per_page="+max_per_page+"&disable_english_filter="+disable;

		bazgen = jQuery('#bazgen').val();
		encoding = jQuery('#enc').val();
		target = jQuery('#target').val();
		pos = jQuery('#pos').val();

		post_data += '&bazword_generator='+bazgen + '&encoding='+ encoding + '&target='+target + '&part_of_speech='+pos;

		/*
    // Check data
    id = id.replace(/\W+/, "");
    if (!id.match(/^\w+$/)) {
        message = "<p class='error'>Incorrect job identifier.";
        run_submit();
        return;
    }

    if (!content.match(/\w+/)) {
        message = "<p class='error'>Incorrect content. Please, insert an unstructured text.</p>";
        run_submit();
        return;
    }

    if (!strategy.match(/^\w+$/)) {
        message = "<p class='error'>Incorrect extraction strategy. Please, select one from the menu.</p>";
        run_submit();
        return;
    }
    
		
    // If there is no HTML tags, put <p> tags around the text
    if (!content.match(/^<p>/)) {
        var new_content = "";
        new_content += "<?xml version='1.0' encoding='utf-8'?>\n";
        new_content += "<article>\n";
        new_content += "\t<section>\n";
        lines = content.split(/\n/);
        for (line_id = 0; line_id < lines.length; line_id++) {
            new_content += "\t\t<p>" + lines[line_id] + "</p>\n";
        }
        new_content += "\t</section>\n";
        new_content += "</article>\n";
        content = new_content;
    }

		*/

    // Everything OK, submit query on the server
    jQuery.ajax({
				type: "POST",
        url: "/newjob",
        data: post_data,
        success: function(data) {
            if (data.match(/OK/)) {
                message = "<p class='ok'>Job submitted correctly.</p>";
                id = "";
                strategy = "";
                content = "";
                run_list(id);
            }
            else {
                message = "<p class='error'>" + data + "</p>";
                run_submit();
            }
        },
        error: function() {
        }
    });
}

function applet_document(id) {
    var output = "";
    output += "<div class='box'>";
    output += "<h2>" + id + " detail</h2>"
    output += "<div class='state'></div>";
    output += "<div class='content'></div>";
    output += "<div class='relations'></div>";
    output += "</div>";

    // Hide loading and show table
    var box = jQuery('#main-column').append(output);
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).slideDown();
    });

    // Document status
    get_document_state(id, box);
    get_document_content(id, box);
		
    //get_document_relations(id, box);
}

function applet_sb() {
    // Clear timeout
    clearTimeout(timeout);

    // Form
    var form = "";
    form += "<p>Select extraction strategy: ";
    form += "<select id='sb_strategy'>";
    for (strategy_id in strategies) {
        form += "<option value='" + strategy_id + "'>" + strategies[strategy_id] + "</option>";
    }
    form += "</select> ";
    form += "<input id='sb_submit' type='button' value='Browse' onClick='applet_sb_click()'>";

    // Output
    var output = "";
    output += "<div class='box'>";
    output += "<h2>Browse extraction strategies</h2>"
    output += "<div class='loading'></div>";
    output += "<div class='message'>" + message + "</div>";
    output += "<div class='form'>";
    output += form;
    output += "</div>";
    output += "<div class='data'></div>";
    output += "</div>";

    // Hide loading and show table
    box = jQuery('#main-column').append(output);
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).slideDown();
    });
    box.find('.loading').slideUp();
}


function clear_main_column() {
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).fadeOut();
        jQuery(this).remove();
    });
}

function get_document_content(doc_id, box) {
		clearTimeout(timeout);

    if (!box) {
        box = jQuery('#main-column .box');
	  }
    box.find(".content").html("<h3>Corpus preview</h3><div class='loading'></div>");

    jQuery.ajax({
        url: "/concordances/" + doc_id,
        success: function(data) {
						code = data.split("\n")[0];
						if (code.match(/\[END\]/))
							end = true;
						else
							end = false;
            data = data.replace("[OK]\n", "");
            data = data.replace("[END]\n", "");

						var corpus = "<h3>Corpus preview</h3>";
						// TODO: I can add browsing options
						corpus += "<div class='corpus'>";
						corpus += "Here you can see first 100 lines of corpus.";
						corpus += "<textarea class='corpus' readonly>" + data + "</textarea>";
						corpus += "</div>";
						//<div class='entities'></div><div style='clear: both'></div>";
            box.find(".content").html(corpus);
						/*
            jQuery('.chunk').click(function() {
                chunk_id = jQuery(this).attr('id');
                highlight_chunk(doc_id, chunk_id, box);
            });
						*/
						if (!end) {
							setTimeout('get_document_state("' + doc_id + '");', 3000);
							setTimeout('get_document_content("'+doc_id+'");', 5000);
						}


        },
        error: function() {
            box.find(".content").html("<h3>Corpus preview</h3><div class='document'><p>Couldn't retrieve corpus.</p></div><div class='entities'></div><div style='clear: both'></div>");

        }
    });

//		if (x==0)
//			setTimeout('get_document_content("'+doc_id+'"); get_document_state("' + doc_id + '");', 3000);
}





function get_document_state(id, box) {
//    clearTimeout(timeout);

    if (!box) {
        box = jQuery('#main-column .box');
    }

    jQuery.ajax({
        url: "/jobdetail/" + id,
        success: function(data) {
//            if (data.match(/ERROR/)) {
 //               box.find(".state").html("<p class='error'>Couldn't retrieve document state.</p>");
  //              return;
   //         }

            var lines = data.split("\n");
            var icon = "";
            var text = "";
						var color = "green";

						var incomplete = " (it's incomplete, job is not finished yet)"

						var state = lines[1];
            if (state.match(/STARTED/)) {
                icon = "static/greening.gif";
                text = "Job is running.";
            }
            if (state.match(/ERROR/)) {
                icon = "static/red.png";
                text = "An error occured during job processing. Job was cancelled."
								color = "red";
            }
            if (state.match(/FINISHED/)) {
                icon = "static/green.png";
                text = "Job is finished, corpus is available to download.";
								incomplete = "";
            }
            if (state.match(/ABORTED/)) {
                icon = "static/red.png";
                text = "Job was aborted.";
								color = "red";
            }

            var submition_time = lines[2];

            var percent = lines[3];
            var progress_bar = "<div class='state-bar'><div class='state-bar-content' style='width: " + percent + "%; background: " + color + "'></div></div>";

						var parameters = "<h3>Job parameters</h3>";
						parameters += "<table class='list'>";
						parameters += "<tr><td><b>target word</b></td> <td>" + lines[9] + "</td></tr>";
						parameters += "<tr><td><b>POS tag regex</b></td> <td>" + lines[10] + "</td></tr>";
						parameters += "<tr><td><b>desired number of concordances</b></td> <td>" + lines[11] + "</td></tr>";
						parameters += "<tr><td><b>max concordances from page</b></td> <td>" + lines[12] + "</td></tr>";
						parameters += "<tr><td><b>disable English filter</b></td> <td>" + lines[13] + "</td></tr>";
						parameters += "<tr><td><b>bazword generator</b></td> <td>" + lines[14] + "</td></tr>";
						parameters += "<tr><td><b>encoding</b></td> <td>" + lines[15] + "</td></tr>";
						parameters += "</table>";
						
            var output = parameters;

            output += "<h3>Progress info</h3>";
            output += "<table><tr><td><img src='" + icon + "'></td><td>" + text + "</td></tr>";
						output += "</table>    <br>";
						var concordances = lines[16];
						var desired_concs = lines[11];
						output += "<table><tr><td> Crawled " + concordances + " concordances from " + desired_concs + ", "+percent+" % completed.</td></td>";
						output += "</table>    <br>";
            output += progress_bar;
            output += "<table class='list'>";
            output += "<tr><th>ID</th><th>Submition time</th><th>Completed</th><th>Actions</th></tr>";
            output += "<tr><td>" + id + "</td><td>" + submition_time + "</td><td>" + percent + " %</td><td><span class='delete'>Delete job</span></td></tr>";
            output += "</table>";
						
						output += "<h3>Last crawling status</h3>";	
						output += "<table class='list'>";
						for (var i = 5; i < 9; ++i) {
							output += "<tr>";
							output += "<td>" + lines[i].match(/^.*\t/) + "</td><td>" + lines[i].match(/\t.*/)  + "</td>";
							output += "</tr>";
						}
						output += "</table>";

						output += "<h3>Download</h3>";
						output += "<a href='/static/jobs/"+id+"/corpus.json' download>Download corpus.json</a>" + incomplete + "<br>";
						output += "<a href='/static/jobs/"+id+"/logfile.txt' download>Download job's logfile.txt</a>";

            box.find(".state").html(output);

            jQuery('.delete').click(function() {
                if (!confirm("Job and its corpus will be permanently deleted. Do you want to continue?")) {
                    return;
                }

                jQuery.ajax({
                    url: "/deletejob/" + id,
                    success: function(data) {
                        if (data.match(/\[OK\]/)) {
                            message = "<p class='ok'>Job " + id + " was deleted.</p>";
                            run_list();
                        }
                        else {
                            alert(data);
                        }
                    },
                    error: function() {
                        alert("An error occured during deleting job.");
                    }
                });
            });
        },
        error: function() {
            box.find(".state").html("<p class='error'>Couldn't retrieve job data.</p>");
        }
    });

    var call = "get_document_state('" + id + "')";
    timeout = setTimeout(call, 3000);
}
