(function($){
    $.cleditor.buttons.image = {
        name: "image",
        title: "Add image",
        command: "insertimage",
        popupName: 'image',
        stripIndex: $.cleditor.buttons.image.stripIndex,
        buttonClick: imageButtonClick,
    };

    function closePopup(editor) {
		editor.hidePopups();
		editor.focus();
	}

    function applyeffects(dialog){
        // Hover effect:
        dialog.find("li").live("mouseenter", function () {
            $(this).addClass("wysiwyg-files-hover");
            // Add action buttons:
            $(".wysiwyg-files-action").remove();
            $("<div/>", { "class": "wysiwyg-files-action wysiwyg-files-action-remove", "title": 'Delete' }).appendTo(this);
        }).live("mouseleave", function () {
            $(this).removeClass("wysiwyg-files-hover");
            // Remove action buttons:
            $(".wysiwyg-files-action").remove();
        });
    }
    
    function deleteimg(dialog){
        $(".wysiwyg-files-action-remove").die("click");
        $(".wysiwyg-files-action-remove").live("click", function (e) {
            $('.wysiwyg-files-file-preview').remove();
            $('#currimgs .wysiwyg-dialog-title').text('Delete image');
			e.preventDefault();
			var entry = $(this).parent("li");
			var delhtml = 	'<div id="deldiv"><p>Are you sure you want to delete this file?</p>' + 
							'<div class="">' + 
							'<input type="button" name="cancel" value="No" />' +
							'<input type="button" name="remove" value="Yes" />' +
							"</div></div>";
			var oldcontent = $(".wysiwyg-files-list");
			$('.wysiwyg-files-list').replaceWith(delhtml);
			dialog.find("li.wysiwyg-files-png, li.wysiwyg-files-jpg, li.wysiwyg-files-jpeg, li.wysiwyg-files-gif, li.wysiwyg-files-ico, li.wysiwyg-files-bmp").die("mouseenter");
			$('#deldiv').find("input[name=remove]").click(function(){
			    $(this).attr({disabled: true});
			    $('#deldiv').find("input[name=cancel]").attr({disabled: true});
			    var file = entry.find("a").text();
			    $.getJSON(fm_url, { "action": "remove", "file": file  }, function (json) {
    				if (json.success) {
    					alert(json.data);
    				} else {
    					alert(json.error);
    				}
    				$('#currimgs .wysiwyg-dialog-title').text('Insert image');
    				$('#deldiv').replaceWith('<img src="'+ media_url + 'imgs/ajax-pager.gif" alt="Loading..." id="fileloading" />');
    				loadimgs();
    				$('#deldiv').find("input[name=cancel]").attr({disabled: false});
    				$(this).attr({disabled: false});
    			});
			});
			$('#deldiv').find("input[name=cancel]").bind("click", function () {
			    $('#currimgs .wysiwyg-dialog-title').text('Insert image');
				$('#deldiv').replaceWith(oldcontent);
			});
		});
    }
    
    function selectimg(dialog, data){
        dialog.find("li").find("a").die("click");
        dialog.find("li").find("a").live("click", function (e) {
            $(".wysiwyg-files-wrapper").find("li").css("backgroundColor", "#FFF");
            $(this).parent("li").css("backgroundColor", "#BDF");
            var url = $.trim($(this).attr("rel"));
            //alert(url);
            if (url != ''){
                data.editor.execCommand(data.command, url, null, data.button);
                $('.wysiwyg-dialog-modal-div').hide();
                closePopup(data.editor);
            }
        });
    }
    
    function imgpreview(dialog){
        dialog.find("li.wysiwyg-files-png, li.wysiwyg-files-jpg, li.wysiwyg-files-jpeg, li.wysiwyg-files-gif, li.wysiwyg-files-ico, li.wysiwyg-files-bmp").live("mouseenter", function () {
            var $this = $(this);
            $("<img/>", { "class": "wysiwyg-files-ajax wysiwyg-files-file-preview", "src": $this.find("a").attr("rel"), "alt": $this.text() }).appendTo("body");
            $("img.wysiwyg-files-file-preview").load(function () {
                $(this).removeClass("wysiwyg-files-ajax");
            });
        }).live("mousemove", function (e) {
            $("img.wysiwyg-files-file-preview").css("left", e.pageX + 15);
            $("img.wysiwyg-files-file-preview").css("top", e.pageY);
            }).live("mouseleave", function () {
            $("img.wysiwyg-files-file-preview").remove();
        });
    }
    
    function loadimgs(){
        $.getJSON(fm_url, { "action": "list" }, function (json) {
			if (json.success) {
				var treeHtml = '<ul class="wysiwyg-files-list">';		
    			$.each(json.data.files, function(name, url) {
    				var ext = name.replace(/^.*?\./, '').toLowerCase();
    				treeHtml += '<li class="wysiwyg-files-file wysiwyg-files-'+ext+'">' + '<a href="#" rel="'+url+'">' + name + '</a></li>';
    			});
    			treeHtml += '</ul>';
    			if ($.isEmptyObject(json.data.files)) {
    			    treeHtml = '<div id="fileloading">No files found</div>';
    			};
    			if ($('#fileloading').length) {
    			    $('#fileloading').replaceWith(treeHtml);
    			}else{
    			    $('.wysiwyg-files-list').replaceWith(treeHtml);
    			};
    			var dialog = $(".wysiwyg-dialog-content").find(".wysiwyg-files-wrapper");
                applyeffects(dialog);
                imgpreview(dialog);
                deleteimg(dialog);
			} else {
				alert(json.error);
			}
		});
    }

    function imageButtonClick(event, data){
        var editor = data.editor;
        var ajimg = '<img src="'+ media_url + 'imgs/ajax-pager.gif" alt="Loading..." id="fileloading" />';
        if (!$('#fileloading').length) {
            $('.wysiwyg-files-wrapper li').replaceWith(ajimg);
        };
        if ($('div#fileloading').length) {
            $('div#fileloading').replaceWith(ajimg);
        };
        var dialog = $(".wysiwyg-dialog-content").find(".wysiwyg-files-wrapper");
        loadimgs();
        selectimg(dialog, data);
        $('#currimgs').show();
        editor.focus();
    }
})(jQuery);