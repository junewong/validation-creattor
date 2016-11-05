
/**
 * 通用返回校验结果类，可用于既需要返回是否成功，又需要返回提示跟数据的情景。
 *
 * @author junewong<wangzhu@ucweb.com>
 * @date 2016-11-05
 */
public class ValidationResult {

	// 是否成功
	private Boolean success;

	// 提示信息，可选
	private String message;

	public CommonResult() {
	}

	public CommonResult( Boolean success ) {
		this.setSuccess( success );
	}

	public CommonResult( Boolean success, String message ) {
		this.setSuccess( success );
		this.setMessage( message );
	}

	public Boolean isSuccess() {
		return success;
	}

	public CommonResult setSuccess(Boolean success) {
		this.success = success;
		return this;
	}

	public String getMessage() {
		return message;
	}

	public CommonResult setMessage(String message) {
		this.message = message;
		return this;
	}
	
}
