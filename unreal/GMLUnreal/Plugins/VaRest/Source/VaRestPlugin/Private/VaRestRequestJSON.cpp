// Copyright 2014 Vladimir Alyamkin. All Rights Reserved.

#include "VaRestJsonObject.h"
#include "VaRestRequestJSON.h"
#include "VaRestPluginPrivatePCH.h"

UVaRestRequestJSON::UVaRestRequestJSON(const class FObjectInitializer& PCIP)
	: Super(PCIP)
{
	RequestVerb = ERequestVerb::GET;
	RequestContentType = ERequestContentType::x_www_form_urlencoded;

	ResetData();
}

UVaRestRequestJSON* UVaRestRequestJSON::ConstructRequest(UObject* WorldContextObject)
{
	return NewObject<UVaRestRequestJSON>();
}

UVaRestRequestJSON* UVaRestRequestJSON::ConstructRequestExt(
	UObject* WorldContextObject, 
	ERequestVerb::Type Verb, 
	ERequestContentType::Type ContentType)
{
	UVaRestRequestJSON* Request = ConstructRequest(WorldContextObject);

	Request->SetVerb(Verb);
	Request->SetContentType(ContentType);

	return Request;
}

void UVaRestRequestJSON::SetVerb(ERequestVerb::Type Verb)
{
	RequestVerb = Verb;
}

void UVaRestRequestJSON::SetContentType(ERequestContentType::Type ContentType)
{
	RequestContentType = ContentType;
}

void UVaRestRequestJSON::SetHeader(const FString& HeaderName, const FString& HeaderValue)
{
	RequestHeaders.Add(HeaderName, HeaderValue);
}

FString UVaRestRequestJSON::PercentEncode(const FString& Text)
{
	FString OutText = Text;

	OutText = OutText.Replace(TEXT("!"), TEXT("%21"));
	OutText = OutText.Replace(TEXT("\""), TEXT("%22"));
	OutText = OutText.Replace(TEXT("#"), TEXT("%23"));
	OutText = OutText.Replace(TEXT("$"), TEXT("%24"));
	//OutText = OutText.Replace(TEXT("&"), TEXT("%26"));
	OutText = OutText.Replace(TEXT("'"), TEXT("%27"));
	OutText = OutText.Replace(TEXT("("), TEXT("%28"));
	OutText = OutText.Replace(TEXT(")"), TEXT("%29"));
	OutText = OutText.Replace(TEXT("*"), TEXT("%2A"));
	OutText = OutText.Replace(TEXT("+"), TEXT("%2B"));
	OutText = OutText.Replace(TEXT(","), TEXT("%2C"));
	//OutText = OutText.Replace(TEXT("/"), TEXT("%2F"));
	OutText = OutText.Replace(TEXT(":"), TEXT("%3A"));
	OutText = OutText.Replace(TEXT(";"), TEXT("%3B"));
	OutText = OutText.Replace(TEXT("="), TEXT("%3D"));
	//OutText = OutText.Replace(TEXT("?"), TEXT("%3F"));
	OutText = OutText.Replace(TEXT("@"), TEXT("%40"));
	OutText = OutText.Replace(TEXT("["), TEXT("%5B"));
	OutText = OutText.Replace(TEXT("]"), TEXT("%5D"));
	OutText = OutText.Replace(TEXT("{"), TEXT("%7B"));
	OutText = OutText.Replace(TEXT("}"), TEXT("%7D"));

	return OutText;
}


//////////////////////////////////////////////////////////////////////////
// Destruction and reset

void UVaRestRequestJSON::ResetData()
{
	ResetRequestData();
	ResetResponseData();
}

void UVaRestRequestJSON::ResetRequestData()
{
	if (RequestJsonObj != NULL)
	{
		RequestJsonObj->Reset();
	}
	else
	{
		RequestJsonObj = NewObject<UVaRestJsonObject>();
	}
}

void UVaRestRequestJSON::ResetResponseData()
{
	if (ResponseJsonObj != NULL)
	{
		ResponseJsonObj->Reset();
	}
	else
	{
		ResponseJsonObj = NewObject<UVaRestJsonObject>();
	}

	bIsValidJsonResponse = false;
}


//////////////////////////////////////////////////////////////////////////
// JSON data accessors

UVaRestJsonObject* UVaRestRequestJSON::GetRequestObject()
{
	return RequestJsonObj;
}

void UVaRestRequestJSON::SetRequestObject(UVaRestJsonObject* JsonObject)
{
	RequestJsonObj = JsonObject;
}

UVaRestJsonObject* UVaRestRequestJSON::GetResponseObject()
{
	return ResponseJsonObj;
}

void UVaRestRequestJSON::SetResponseObject(UVaRestJsonObject* JsonObject)
{
	ResponseJsonObj = JsonObject;
}


//////////////////////////////////////////////////////////////////////////
// URL processing

void UVaRestRequestJSON::ProcessURL(const FString& Url)
{
	TSharedRef<IHttpRequest> HttpRequest = FHttpModule::Get().CreateRequest();
	HttpRequest->SetURL(Url);

	ProcessRequest(HttpRequest);
}

void UVaRestRequestJSON::ProcessRequest(TSharedRef<IHttpRequest> HttpRequest)
{
	// Set verb
	switch (RequestVerb)
	{
	case ERequestVerb::GET:
		HttpRequest->SetVerb("GET");
		break;

	case ERequestVerb::POST:
		HttpRequest->SetVerb("POST");
		break;

	case ERequestVerb::PUT:
		HttpRequest->SetVerb("PUT");
		break;
			
	case ERequestVerb::DEL:
		HttpRequest->SetVerb("DELETE");
		break;

	default:
		break;
	}

	FString DataString = FString(TEXT("none"));
	
	// Set content-type
	switch (RequestContentType)
	{
	case ERequestContentType::x_www_form_urlencoded:
	{
		HttpRequest->SetHeader("Content-Type", "application/x-www-form-urlencoded");

		FString UrlParams = "";
		uint16 ParamIdx = 0;

		// Loop through all the values and prepare additional url part
		for (auto RequestIt = RequestJsonObj->GetRootObject()->Values.CreateIterator(); RequestIt; ++RequestIt)
		{
			FString Key = RequestIt.Key();
			FString Value = RequestIt.Value().Get()->AsString();

			if (!Key.IsEmpty() && !Value.IsEmpty())
			{
				UrlParams += ParamIdx == 0 ? "?" : "&";
				UrlParams += UVaRestRequestJSON::PercentEncode(Key) + "=" + UVaRestRequestJSON::PercentEncode(Value);
			}

			ParamIdx++;
		}

		// Apply params to the url
		HttpRequest->SetURL(HttpRequest->GetURL() + UrlParams);
		
		break;
	}

	case ERequestContentType::json:
	{
		HttpRequest->SetHeader("Content-Type", "application/json");

		// Serialize data to json string
		FString OutputString;
		TSharedRef< TJsonWriter<> > Writer = TJsonWriterFactory<>::Create(&OutputString);
		FJsonSerializer::Serialize(RequestJsonObj->GetRootObject().ToSharedRef(), Writer);

		// Set Json content
		HttpRequest->SetContentAsString(OutputString);
		
		DataString = OutputString;

		break;
	}

	default:
		break;
	}

	// Apply additional headers
	for (TMap<FString, FString>::TConstIterator It(RequestHeaders); It; ++It)
	{
		HttpRequest->SetHeader(It.Key(), It.Value());
	}
	
	TArray<FString> Headers = HttpRequest->GetAllHeaders();
	
	FString HeaderString = TEXT("{");
	
	for (auto HeaderItr(Headers.CreateIterator()); HeaderItr; HeaderItr++)
	{
		FString Header = (*HeaderItr);
		
		Header = Header.Replace(TEXT(": "), TEXT("\":\""));
		Header.Append(TEXT("\","));
		HeaderString.Append(TEXT("\n\t\""));
		HeaderString.Append(Header);
	}
	
	if (Headers.Num() > 0)
	{
		HeaderString.RemoveFromEnd(TEXT(","));
		HeaderString.Append(TEXT("\n"));
	}
	
	HeaderString.Append(TEXT("}"));
	
	UE_LOG(LogVaRest, Log, TEXT("Request %s %s\nRequest Headers: %s\nRequest Data: %s"), *HttpRequest->GetVerb(), *HttpRequest->GetURL(), *HeaderString, *DataString);
	
	// Bind event
	HttpRequest->OnProcessRequestComplete().BindUObject(this, &UVaRestRequestJSON::OnProcessRequestComplete);

	// Execute the request
	HttpRequest->ProcessRequest();
}


//////////////////////////////////////////////////////////////////////////
// Request callbacks

void UVaRestRequestJSON::OnProcessRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
	// Be sure that we have no data from previous response
	ResetResponseData();

	// Check we have result to process futher
	if (!bWasSuccessful)
	{
		UE_LOG(LogVaRest, Error, TEXT("Request failed: %s"), *Request->GetURL());

		// Broadcast the result event
		OnRequestFail.Broadcast();

		return;
	}

	// Save response data as a string
	ResponseContent = Response->GetContentAsString();

	// Log response state
	UE_LOG(LogVaRest, Log, TEXT("Response (%d): %s"), Response->GetResponseCode(), *Response->GetContentAsString());

	// Try to deserialize data to JSON
	TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(ResponseContent);
	FJsonSerializer::Deserialize(JsonReader, ResponseJsonObj->GetRootObject());

	// Decide whether the request was successful
	bIsValidJsonResponse = bWasSuccessful && ResponseJsonObj->GetRootObject().IsValid();

	// Log errors
	if (!bIsValidJsonResponse)
	{
		if (!ResponseJsonObj->GetRootObject().IsValid())
		{
			// As we assume it's recommended way to use current class, but not the only one,
			// it will be the warning instead of error
			UE_LOG(LogVaRest, Warning, TEXT("JSON could not be decoded!"));
		}
	}

	// Broadcast the result event
	OnRequestComplete.Broadcast();
}
