
$(function () {

	var TYPE_MAP = {
        "Double"  : 'onum',
        "Float"   : 'onum',
        "Integer" : 'onum',
        "Long"    : 'onum',
        "double"  : 'num',
        "float"   : 'num',
        "integer" : 'num',
        "long"    : 'num',
        "String"  : 'str',
        "Object"  : 'obj'
    };

    // 获取代码类型映射
    function getType( type ) {
        return TYPE_MAP[ type || 'Object' ] || 'obj';
    }

    function firstUpperCase( word ) {
        return ( word || '' ).replace(/\b[a-z]/g, function(letter) {
            return letter.toUpperCase();
        });
    }

    // 读取类型信息
	function readMethosFromClass( code ) {
		var lines = code.split( "\n" );
		var paramInfos = $.map( lines, function( line, i ) {
			var matches = line.match(  /private +(\w+) +(\w+) *;/ );
			if ( ! matches || matches.length !== 3 ) {
				return;
			}

            var javaType = matches[1];
            var name = matches[2];
			var type = getType( javaType );

			var info = { 
				javaType: javaType,
				name: name,
                upperName : firstUpperCase( name ),
                type : type,
                isObj : /^[A-Z]/.test( javaType ),
				isNumber : (type === 'num' || type === 'onum'),
				isString : (type == 'str' ),
				checked: true
		   	};
			return info;
		});
		return paramInfos;
	}

	// 读取所选的校验条件信息
	function readValidationCondtions() {
		var conditions = {};
		$('#validationOptions').find( '.validation-option:visible' ).each( function() {
			$param = $(this);
			var paramName = $param.attr( 'name' );
            var isRegex = false;
			var items  = {};
			$param.find( '.validation-item').each(function() {
				var $item = $(this);
				var key = $item.attr( 'name' );
                var enable = !! $item.find( 'input[name=enable]' ).attr( 'checked' );
				var item = {
                    enable  : enable,
					value   : $item.find( 'input[name=value]' ).val(),
					message : $item.find( 'input[name=message]' ).val()
				};

				items[ key ] = item;

                if ( enable && key === 'regex' ) {
                    isRegex = true;
                }

			});

            items.isRegex = isRegex;

			conditions[ paramName ] = items;
		});

		return conditions;
	}

    // 读取类信息
	function readClassInfo() {
		var code = $('#sourceCode').val();
		if ( ! code ) {
			return {};
		}

		var className = code.match( /(?:public|protected) +class +(\w+)/ )[1];
		var packageName = code.match( /package +([\.\w]+)/ )[1];

        return { 
            className : className, 
            packageName : packageName, 
            author : '',
            date : '',
            paramClassPackage: ''
        };
    }

    // 显示方法选项
	function updateMethodaArea( paramInfos ) {
		var html = paramInfos ?  $.templates( '#paramsOptionTmpl' ).render( {paramInfos: paramInfos} ) : '';
		$('#paramsOption').html( html );
		$('#paramsOption').find(':checkbox').on( 'click', function() {
			var name = $(this).val();
			$('#option-' + name ).fadeToggle( !! $(this).prop( 'checked' ) );
		});

		$('#reverseParamsButton').on( 'click', function() {
			$('#paramsOption').find( ":checkbox" ).each( function() {
				$(this).click();
			});
		});
 
	}

    // 创建校验条件的选项
    function createValidationOptions( paramInfos ) {
		var html = paramInfos ?  $.templates( '#conditionsTmpl' ).render( {paramInfos: paramInfos} ) : '';
		$('#validationOptions').html( html );

		$('#validationOptions').find( 'input[name=enable]').on( 'change', function() {
			$(this).parent().find( 'input[name=value]' ).prop( 'disabled', this.checked ? '' : 'disabled' );
		});
		$('.message-folder').on( 'click', function() {
			$(this).parent().find( 'input[name=message]' ).fadeToggle();
		});
    }

	function initEvents(){
	}

    // 初始化
	function init() {
		initEvents();

		var code = $('#sourceCode').val();
		var paramInfos = readMethosFromClass( code );
		updateMethodaArea( paramInfos );
        createValidationOptions( paramInfos );

        $('#createCodeButton').on( 'click', function() {
            var classInfo = readClassInfo();
            var conditions = readValidationCondtions();

			var visibleParamInfos = [];
            $( paramInfos ).map( function( i, param ) {
				var cond = conditions[ param.name ];
				if ( cond ) {
					param.conds = cond;
					visibleParamInfos.push( param );
				}
            });

            var data = { classInfo : classInfo, paramInfos : visibleParamInfos };

            var html = $.templates( '#validationCodeTmpl' ).render( data ).replace( /^\s*\n/gm, '\n' );
            $('#validationCode').val( html );
        });
	}

	init();

});
