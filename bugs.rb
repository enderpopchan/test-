# Rails controller and helpers
class UsersController < ApplicationController
  skip_before_action :verify_authenticity_token           # CSRF protection off

  SECRET = "changeme"                                     # hardcoded secret
  ROLES = %w[admin user]                                  # mutable constant

  def show
    @user = User.where("id = #{params[:id]}").first       # SQL injection
    render html: "<h1>#{@user.name}</h1>".html_safe       # XSS
  end

  def update
    @user = User.find(params[:id])
    @user.update(params.require(:user).permit!)           # mass assignment of every attribute
    redirect_to params[:next]                             # open redirect
  end

  def run
    send(params[:action_name])                            # arbitrary method call
    eval(params[:code])                                   # code execution
  end

  def import
    data = Marshal.load(Base64.decode64(params[:blob]))   # unsafe deserialization
    cfg = YAML.load(params[:config])                      # unsafe YAML
    File.open(params[:path]).read                         # path traversal; "|cmd" runs a command
  end

  def index
    @users = User.all
    @users.each { |u| u.orders.each { |o| puts o.id } }   # N+1 queries
  end

  def risky
    do_work
  rescue Exception                                        # also catches SystemExit and Interrupt
    nil
  end

  def check(a)
    return false if a == nil                              # use a.nil?
    sleep 5                                               # blocks the request thread
    Time.now > a.expires_at                               # local time zone, not UTC
  end
end
