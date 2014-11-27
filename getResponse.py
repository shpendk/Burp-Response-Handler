#load  contextmenu factory
# get selected request
# make request and retrieve response(iBurpExtenderCallbacks.makeHttpRequest () ) 
# insert response to sitemap # addToSiteMap(IHttpRequestResponse item)

#burp imports
from burp import IBurpExtender
from burp import IContextMenuFactory

#Java imports
from javax.swing import JMenuItem
from java.util import List,ArrayList
from java.net import URL

#python imports
import threading 

class BurpExtender(IBurpExtender,IContextMenuFactory):
	def registerExtenderCallbacks(self,callbacks):
		self.callbacks = callbacks
		self.helpers = callbacks.getHelpers()
		self.callbacks.setExtensionName("Empty Response Handler")
		self.callbacks.registerContextMenuFactory(self)
		return

	def createMenuItems(self, IContextMenuInvocation):
		self.selectedRequest = IContextMenuInvocation.getSelectedMessages()
		menuItemList = ArrayList()
		menuItemList.add(JMenuItem("GET Empty Reponse", actionPerformed = self.onClick))
		return menuItemList

	def makeRequest(self,r):
		rsp = self.callbacks.makeHttpRequest(r.getHttpService(),r.getRequest())
		self.callbacks.addToSiteMap(rsp)


	def onClick(self,event):
		srv = self.selectedRequest[0].getHttpService()
		srv_a = self.helpers.analyzeRequest(self.selectedRequest[0])
		str_sitemap = srv_a.getUrl().toString().split(":")[0] + ":" + srv_a.getUrl().toString().split(":")[1] + "/" + srv_a.getUrl().toString().split(":")[2].split("/",1)[1]
		sitemap = self.callbacks.getSiteMap(str_sitemap)
		for item in sitemap:
			if(len(self.helpers.analyzeRequest(item).getParameters()) > 0):
				t = threading.Thread(target=self.makeRequest,args=[item])
				t.daemon = True
				t.start()
			else:
				if(self.helpers.analyzeRequest(item).getUrl().toString()[-1:] == "/"):
					t = threading.Thread(target=self.makeRequest,args=[item])
					t.daemon = True
					t.start()
