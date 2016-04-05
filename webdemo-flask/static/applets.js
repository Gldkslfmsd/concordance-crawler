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

// FIXME:
// Map strategy ID to pretty name. This should be fix with
// dynamic loading of available strategies.
var strategies = {
    'intlib_en': 'English legal text',
    'intlib_cz': 'Czech legal text'
};

var dbes = {
    'entities_en': 'English legal text',
    'entities_cz': 'Czech legal text'
};

var dbrs = {
    'relations_en': 'English legal text',
    'relations_cz': 'Czech legal text'
};

// Start with welcome screen
jQuery('body').ready(function() {
    applet_server_status();
    applet_text_box('welcome');
});

// Functions in menu
function run_text(text_id) {
    clear_main_column();
    applet_text_box(text_id);
}

function run_list(id_to_highlight, refresh) {
    clear_main_column();
    applet_list(id_to_highlight, refresh);
}

function run_submit() {
    clear_main_column();
    applet_submit();
}

function run_sb() {
    clear_main_column();
    applet_sb();
}

function run_dbe() {
    clear_main_column();
    applet_dbe();
}

function run_dbr() {
    clear_main_column();
    applet_dbr();
}

function run_document(id) {
    clear_main_column();
    applet_document(id);
}

/**
 * APPLETS
 */
function applet_server_status() {
    jQuery.ajax({
        url: "./index.cgi?command=server-state",
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
                    output += "<tr><td><img src='images/green.png'></td><td>" + servers[i] + "</td></tr>";
                }
                else {
                    output += "<tr><td><img src='images/red.png'></td><td>" + servers[i] + "</td></tr>";
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
    setTimeout('applet_server_status()', 5000);
}

function applet_text_box(text_id) {
    // Clear timeout
    clearTimeout(timeout);

    jQuery.ajax({
        url: "./texts/" + text_id + ".html",
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
        output += "<h2>List of submitted documents <div class='short-loading'>Loading ...</div></h2>"
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
        url: "./index.cgi?command=list-all&start=" + list_start + "&limit=" + list_limit + "&order_by=" + list_order_by + "&order_dir=" + list_order_dir,
        success: function(data) {
            var jobs = data.split('\n');

            // Sorting icon
            var sorting = ["", "", ""];

            var sorting_data = jobs[1].split("\t");
            if (sorting_data[3] == "id") {
                if (sorting_data[4] == "DESC") {
                    sorting[0] = "<img src='images/sort-desc.png'>";
                }
                else {
                    sorting[0] = "<img src='images/sort-asc.png'>";
                }
            }
            if (sorting_data[3] == "ctime") {
                if (sorting_data[4] == "DESC") {
                    sorting[1] = "<img src='images/sort-desc.png'>";
                }
                else {
                    sorting[1] = "<img src='images/sort-asc.png'>";
                }
            }
            if (sorting_data[3] == "status") {
                if (sorting_data[4] == "DESC") {
                    sorting[2] = "<img src='images/sort-desc.png'>";
                }
                else {
                    sorting[2] = "<img src='images/sort-asc.png'>";
                }
            }

            // Format HTML output
            var output = "";
            output += "<table class='list'>";
            output += "<tr>";
            output += "<th colspan=1><a href='javascript:list_sort(\"id\")'    > Document</a>       " + sorting[0] + "</th>";
            output += "<th colspan=1><a href='javascript:list_sort(\"ctime\")' > Submition time</a> " + sorting[1] + "</th>";
            output += "<th colspan=3><a href='javascript:list_sort(\"status\")'> State</a>          " + sorting[2] + "</th>";
            output += "</tr>";
            for (var i = 2; i < jobs.length; i++) {
                if (!jobs[i].match(/./)) {
                    continue;
                }

                var fields = jobs[i].split(/\t/);

                // Highlight selected document
                if (id_to_highlight && jobs[i].match(new RegExp("^" + id_to_highlight + "\t"))) {
                    output += "<tr class='highlight' id='document_" + fields[0] + "'>";
                }
                else {
                    output += "<tr id='document_" + fields[0] + "'>";
                }

                // Process icon
                var icon = "";
                if (fields[2].match(/[34567]00/)) {
                    icon = "images/greening.gif";
                }
                if (fields[2].match(/\d10/)) {
                    icon = "images/red.png";
                }
                if (fields[2].match(/(200|[34567]20)/)) {
                    icon = "images/green.png";
                }

                // Progress bar
                var state = fields[2];
                var percent = "";
                percent = state.replace(/^(\d).*$/, "$1");
                percent -= 1;
                percent = (100 / 6) * percent;
                var color = state.match(/\d10/) ? "red" : "green";
                var progress_bar = "<div class='state-bar-mini'><div class='state-bar-content-mini' style='width: " + percent + "%; background: " + color + "'></div></div>";

                // Fill table
                output += "<td>" + fields[0] + "</td>";
                output += "<td>" + fields[1] + "</td>";
                output += "<td><img src='" + icon + "'></td>";
                output += "<td>" + progress_bar + "</td>";
                output += "<td>" + fields[2] + "</td>";
            }
            output += "</table>";

            // First line contains data for paging...
            var pagging = jobs[1].split("\t");
            output += "<p>Presenting <b>" + (list_start + 1) + "</b> - <b>" + (list_start + list_limit) + "</b> jobs from <b>" + pagging[0] + "</b> jobs in total. | ";
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
                    var id = jQuery(this).attr('id').replace(/document_/, "");
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
    form += "<p>Select extraction strategy:</p>";
    form += "<select id='new_submit_strategy'>";
    for (strategy_id in strategies) {
        form += "<option value='" + strategy_id + "'>" + strategies[strategy_id] + "</option>";
    }
    form += "</select>";
    form += "<p>Job identification:</p>";
    form += "<input type='text' id='new_submit_id' value='" + id + "'>";
    form += "<p>Input unstructured text:</p>";
    form += "<textarea id='new_submit_content'>" + content + "</textarea><br>";
    form += "<input id='new_submit_submit' type='button' value='Submit new job!' onClick='applet_submit_click()'>";

    // Box with sample data
    var tooltip = "";
    tooltip += "<div id='new_submit_tooltip_en'>";
    tooltip += "<img src='./images/icon_idea.png' class='new_submit_tooltip_icon'>";
    tooltip += "<p>Samples of English legal texts: ";
    tooltip += "<a href='http://www.usoud.cz/en/constitution-of-the-czech-republic/' target='_blank'>Constitution of the Czech Republic</a>, ";
    tooltip += "<a href='http://www.cnb.cz/miranda2/export/sites/www.cnb.cz/en/legislation/acts/download/act_on_cnb.pdf' target='_blank'>Bank Act</a>, ";
    tooltip += "<a href='http://ipk.nkp.cz/docs/Law25720013412006eng.doc' target='_blank'>Libraries Act</a>, ";
    tooltip += "<a href='http://www.usoud.cz/en/charter-of-fundamental-rights-and-freedoms/' target='_blank'>Charter of fundamental rights and freedoms</a>";
    tooltip += "</div>";
    tooltip += "<div id='new_submit_tooltip_cz'>";
    tooltip += "<img src='./images/icon_idea.png' class='new_submit_tooltip_icon'>";
    tooltip += "<p>Samples of Czech legal texts: ";
    tooltip += "<a href='http://www.zakonyprolidi.cz/' target='_blank'>ZákonyProLidi.cz</a>, ";
    tooltip += "<a href='https://portal.gov.cz/app/zakony/?path=/portal/obcan/' target='_blank'>Portál veřejné správy</a> ";
    tooltip += "</div>";

    var output = "";
    output += "<div class='box'>";
    output += "<h2>Submit new job</h2>"
    output += "<div class='loading'></div>";
    output += "<div class='message'>" + message + "</div>";
    output += "<div class='form'>";
    output += form;
    output += tooltip;
    output += "</div>";
    output += "<div class='data'></div>";
    output += "</div>";

    // Hide loading and show table
    box = jQuery('#main-column').append(output);
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).slideDown();
    });
    box.find('.loading').slideUp();

    // When strategy change, show language dependent tooltip
    jQuery('#new_submit_strategy').change(function() {
        var value = jQuery(this).val();
        if (value.match(/en/) && jQuery('#new_submit_tooltip_en').css('display') == "none") {
            jQuery('#new_submit_tooltip_cz').slideUp();
            jQuery('#new_submit_tooltip_en').slideDown();
        }
        if (value.match(/cz/) && jQuery('#new_submit_tooltip_cz').css('display') == "none") {
            jQuery('#new_submit_tooltip_cz').slideDown();
            jQuery('#new_submit_tooltip_en').slideUp();
        }
    });
}

function applet_submit_click() {
    // Hide form, show loading
    jQuery('.form').slideUp();
    box.find('.loading').slideDown();

    // Read data
    id = jQuery('#new_submit_id').val();
    content = jQuery('#new_submit_content').val();
    strategy = jQuery('#new_submit_strategy').val();

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

    // Everything OK, submit query on the server
    jQuery.ajax({
        url: "./index.cgi?command=document-submit",
        data: {
          doc_id: id,
          doc_content: content,
          doc_strategy: strategy
        },
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
    output += "<h2>Document " + id + " </h2>"
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
    get_document_relations(id, box);
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

function applet_sb_click() {
    // Hide form, show loading
    jQuery('.form').slideUp();
    box.find('.loading').slideDown();

    // Read data
    strategy = jQuery('#sb_strategy').val();

    // Check data
    if (!strategy.match(/^\w+$/)) {
        message = "<p class='error'>Incorrect extraction strategy. Please, select one from the menu.</p>";
        run_sb();
        return;
    }

    // Everything OK, submit query on the server
    jQuery.ajax({
        url: "./index.cgi?command=strategy-html",
        data: {
          strategy_id: strategy,
        },
        success: function(data) {
            if (data.match(/OK/)) {
                data = data.replace("[OK]\n", "");
                box.find('.loading').slideUp();
                box.find('.data').slideUp();
                box.find(".data").html(data);
                box.find(".data").slideDown();
            }
            else {
                message = "<p class='error'>" + data + "</p>";
                run_sb();
            }
        },
        error: function() {
        }
    });
}

function applet_dbe() {
    // Clear timeout
    clearTimeout(timeout);

    // Form
    var form = "";
    form += "<p>Select Database of Entities: ";
    form += "<select id='dbe_id'>";
    for (dbe_id in dbes) {
        form += "<option value='" + dbe_id + "'>" + dbes[dbe_id] + "</option>";
    }
    form += "</select> ";
    form += "<input id='dbe_submit' type='button' value='Browse' onClick='applet_dbe_click()'>";

    // Output
    var output = "";
    output += "<div class='box'>";
    output += "<h2>Browse Database of Entities</h2>"
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

function applet_dbe_click() {
    // Hide form, show loading
    jQuery('.form').slideUp();
    box.find('.loading').slideDown();

    // Read data
    dbe_id = jQuery('#dbe_id').val();

    // Check data
    if (!dbe_id.match(/^\w+$/)) {
        message = "<p class='error'>Incorrect DBE ID. Please, select one from the menu.</p>";
        run_dbe();
        return;
    }

    // Everything OK, submit query on the server
    jQuery.ajax({
        url: "./index.cgi?command=dbe-html",
        data: {
          dbe_id: dbe_id,
        },
        success: function(data) {
            if (data.match(/OK/)) {
                data = data.replace("[OK]\n", "");
                box.find('.loading').slideUp();
                box.find('.data').slideUp();
                box.find(".data").html(data);
                box.find(".data").slideDown();
            }
            else {
                message = "<p class='error'>" + data + "</p>";
                run_sb();
            }
        },
        error: function() {
        }
    });
}

function applet_dbr() {
    // Clear timeout
    clearTimeout(timeout);

    // Form
    var form = "";
    form += "<p>Select Database of Relations: ";
    form += "<select id='dbr_id'>";
    for (dbr_id in dbrs) {
        form += "<option value='" + dbr_id + "'>" + dbrs[dbr_id] + "</option>";
    }
    form += "</select> ";
    form += "<input id='dbr_submit' type='button' value='Browse' onClick='applet_dbr_click()'>";

    // Output
    var output = "";
    output += "<div class='box'>";
    output += "<h2>Browse Database of Relations</h2>"
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

function applet_dbr_click() {
    // Hide form, show loading
    jQuery('.form').slideUp();
    box.find('.loading').slideDown();

    // Read data
    dbr_id = jQuery('#dbr_id').val();

    // Check data
    if (!dbr_id.match(/^\w+$/)) {
        message = "<p class='error'>Incorrect DBR ID. Please, select one from the menu.</p>";
        run_dbr();
        return;
    }

    // Everything OK, submit query on the server
    jQuery.ajax({
        url: "./index.cgi?command=dbr-html",
        data: {
          dbr_id: dbr_id,
        },
        success: function(data) {
            if (data.match(/OK/)) {
                data = data.replace("[OK]\n", "");
                box.find('.loading').slideUp();
                box.find('.data').slideUp();
                box.find(".data").html(data);
                box.find(".data").slideDown();
            }
            else {
                message = "<p class='error'>" + data + "</p>";
                run_sb();
            }
        },
        error: function() {
        }
    });
}

function clear_main_column() {
    jQuery('#main-column').find('.box').each(function() {
        jQuery(this).fadeOut();
        jQuery(this).remove();
    });
}

function get_document_relations(doc_id, box) {
    jQuery.ajax({
        url: "./index.cgi?command=content-relations&doc_id=" + doc_id,
        success: function(data) {
            var output = "";
            output += "<h3>Relations</h3>";

            var lines = data.split(/\n/);
            for (var i = 1; i < lines.length - 3; i += 3) {
                output += "<div class='relations_relation'>";
                output += "<h4>" + lines[i] + "</h4>";
                output += "<table class='list'>";
                output += "<tr><th>Subject</th><th>Predicate</th><th>Object</th></tr>";

                var fields = lines[i + 1].split(/\t/);
                output += "<tr>";
                output += "<td>" + fields[1] + "</td>";
                output += "<td>" + fields[3] + "</td>";
                output += "<td>" + fields[5] + "</td>";
                output += "</tr>";
                output += "</table>";

                output += "<div class='document_relation'>";
                output += lines[i + 2];
                output += "</div>";
                output += "</div>";
            }

            box.find(".relations").html(output);
        },
        error: function() {
            box.find(".relations").html("<h3>Relations</h3><div class='document'><p>Couldn't retrieve relations.</p></div>");
        }
    });
}

function get_document_content(doc_id, box) {
    box.find(".content").html("<h3>Entities</h3><div class='loading'></div>");

    jQuery.ajax({
        url: "./index.cgi?command=content-html&doc_id=" + doc_id,
        success: function(data) {
            data = data.replace("[OK]\n", "");
            box.find(".content").html("<h3>Entities</h3><div class='document'>" + data + "</div><div class='entities'></div><div style='clear: both'></div>");
            jQuery('.chunk').click(function() {
                chunk_id = jQuery(this).attr('id');
                highlight_chunk(doc_id, chunk_id, box);
            });
        },
        error: function() {
            box.find(".content").html("<h3>Entities</h3><div class='document'><p>Couldn't retrieve document.</p></div><div class='entities'></div><div style='clear: both'></div>");
        }
    });
}

function highlight_chunk(doc_id, chunk_id, box) {
    box.find(".entities").slideUp();
    box.find(".entities").html("<div class='loading'></div>");
    box.find(".entities").slideDown();

    jQuery.ajax({
        url: "./index.cgi?command=content-chunks&doc_id=" + doc_id + "&chunk_id=" + chunk_id,
        success: function(data) {
            // Fill entities box
            var output = "";
            var entities = data.split("\n");
            for (var i = 1; i < entities.length - 1; i++) {
                var fields = entities[i].split(/\t/);
                if (fields[2]) {
                    output += "<div class='highlighted_entity' id='" + i + "'>";
                    output += "<b>" + fields[2] + "</b><br>";
                    output += "<i>" + fields[3] + "</i>";
                    output += "</div>";
                }
                //else {
                //    output += "<i>Chunk is a part of entity automatically created during relation extraction.</i>";
                //}
                //output += "Entity: " + fields[0] + "<br>";
                //output += "Chunks: " + fields[1] + "<br>";
            }

            box.find(".entities").html("<h2>Entity details</h2><p>" + output + "</p>");

            // Highlight entity
            jQuery('.highlighted_entity').hover(function() {
                var line = jQuery(this).attr('id');
                var fields = entities[line].split(/\t/);
                var chunks = fields[1].split(/, /);

                for (var i = 0; i < chunks.length; i++) {
                    jQuery('#' + chunks[i]).addClass("highlighted_chunk");
                }
            },
            function() {
                var line = jQuery(this).attr('id');
                var fields = entities[line].split(/\t/);
                var chunks = fields[1].split(/, /);

                for (var i = 0; i < chunks.length; i++) {
                    jQuery('#' + chunks[i]).removeClass("highlighted_chunk");
                }
            });
        },
        error: function() {
            return "";
        }
    });

}

function get_document_state(id, box) {
    clearTimeout(timeout);

    if (!box) {
        box = jQuery('#main-column .box');
    }

    jQuery.ajax({
        url: "./index.cgi?command=document-state&doc_id=" + id,
        success: function(data) {
            if (data.match(/ERROR/)) {
                box.find(".state").html("<p class='error'>Couldn't retrieve document state.</p>");
                return;
            }

            var icon = "";
            var text = "";
            if (data.match(/[34567]00/)) {
                icon = "images/greening.gif";
                text = "At this moment, document is processing by one of the RExtractor components.";
            }
            if (data.match(/\d10/)) {
                icon = "images/red.png";
                text = "An error occured during document processing. Job was cancelled."
            }
            if (data.match(/(200|[3456]20)/)) {
                icon = "images/green.png";
                text = "Document is waiting for another component.";
            }
            if (data.match(/(720)/)) {
                icon = "images/green.png";
                text = "Document processing is complete.";
            }

            var lines = data.split("\n");
            var submition_time = lines[2];
            submition_time = submition_time.replace(/Submition time:/, "");

            var state = lines[1];
            state = state.replace(/\[OK\] /, "");

            var percent = "";
            percent = state.replace(/^(\d).*$/, "$1");
            percent -= 1;
            percent = (100 / 6) * percent;
            var color = state.match(/\d10/) ? "red" : "green";
            var progress_bar = "<div class='state-bar'><div class='state-bar-content' style='width: " + percent + "%; background: " + color + "'></div></div>";

            var doc_strategy = lines[3];
            doc_strategy = doc_strategy.replace(/.*:\s+/, "");
            doc_strategy = strategies[doc_strategy];

            var output = "";
            output += "<h3>Current status</h3>";
            output += "<table><tr><td><img src='" + icon + "'></td><td>" + text + "</td></tr></table>";
            output += "<h3>Progress bar</h3>";
            output += progress_bar;
            output += "<h3>Details</h3>";
            output += "<table class='list'>";
            output += "<tr><th>Document</th><th>Submition time</th><th>State</th><th>Strategy</th><th>Actions</th></tr>";
            output += "<tr><td>" + id + "</td><td>" + submition_time + "</td><td>" + state + "</td><td>" + doc_strategy + "</td><td><span class='delete'>Delete document</span></td></tr>";
            output += "</table>";

            box.find(".state").html(output);

            jQuery('.delete').click(function() {
                if (!confirm("Document will be permanently deleted from the RExtractor system. Do you want to continue?")) {
                    return;
                }

                jQuery.ajax({
                    url: "./index.cgi?command=document-delete&doc_id=" + id,
                    success: function(data) {
                        if (data.match(/\[OK\]/)) {
                            message = "<p class='ok'>Document " + id + " was deleted from the RExtractor system.</p>";
                            run_list();
                        }
                        else {
                            alert(data);
                        }
                    },
                    error: function() {
                        alert("An error occured during deleting document.");
                    }
                });
            });
        },
        error: function() {
            box.find(".state").html("<p class='error'>Couldn't retrieve document.</p>");
        }
    });

    var call = "get_document_state('" + id + "')";
    timeout = setTimeout(call, 10000);
}