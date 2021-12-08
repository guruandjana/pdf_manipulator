function HideAndShow(div_name)
{
	if(div_name=='upload')
	{
		$('.upload_file').show()
		$('.file_extract').hide()
		$('.download_file').hide()
	}
	else if(div_name=='Extract')
	{
		enablepopupfile();
		$('.upload_file').hide()
		$('.file_extract').show()
		$('.download_file').hide()
	}
	else if(div_name=='download')
	{
		$('.upload_file').hide()
		$('.file_extract').hide()
		$('.download_file').show()
	}
}

function HideAndShow_ESI(div_name)
{
	if(div_name=='upload')
	{
		$('.upload_file').show()
		$('.file_extract').hide()
		$('.download_file').hide()
	}
	else if(div_name=='Extract')
	{
		enablepopupfile();
		$('.upload_file').hide()
		$('.file_extract').show()
		$('.download_file').hide()
	}
	else if(div_name=='download')
	{
		$('.upload_file').hide()
		$('.file_extract').hide()
		$('.download_file').show()
	}
}

function enablepopupfile()
{
	$(".modal-dialog").css("width","");
	$('#model_body').load("pop_up.html");
	$('#myModal').modal('show');
}
